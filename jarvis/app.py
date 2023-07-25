# -*- coding: utf-8 -*-

import json
import logging
import os

try:
    import queue
except ImportError:
    import Queue as queue
try:
    import socketserver
except ImportError:
    import SocketServer as socketserver

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from flask import (
    Flask,
    render_template,
    Response,
    request,
    abort,
    jsonify,
    send_from_directory,
)
from flask_assets import Environment, Bundle
from flask.templating import TemplateNotFound
from jobs import load_jobs
from random import randint


class Jarvis(Flask):
    def __init__(self, name):
        Flask.__init__(self, name)
        self.logger.setLevel(logging.INFO)
        self.jinja_env.trim_blocks = True
        self.jinja_env.lstrip_blocks = True
        self.sched = BackgroundScheduler(logger=self.logger)
        self.queues = {}
        self.last_events = {}
        self.widgets_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "static", "widgets")
        )

    def wsgi_app(self, *args, **kwargs):
        _configure_bundles(self)
        _schedule_jobs(self)
        return super().wsgi_app(*args, **kwargs)


app = Jarvis(__name__)


def _configure_bundles(app):
    js = ["main.js"]
    css = ["main.css"]
    for widget in os.listdir(app.widgets_path):
        widget_path = os.path.join("widgets", widget)
        for asset_file in os.listdir(os.path.join(app.widgets_path, widget)):
            asset_path = os.path.join(widget_path, asset_file)
            if asset_file.endswith(".js"):
                js.append(asset_path)
            elif asset_file.endswith(".css"):
                css.append(asset_path)

    assets = Environment(app)
    if app.debug:
        assets.register("js_all", Bundle(*js, output="gen/app.js"))
        assets.register("css_all", Bundle(*css, output="gen/styles.css"))
    else:
        assets.register(
            "js_min_all", Bundle(*js, filters="rjsmin", output="gen/app.min.js")
        )
        assets.register(
            "css_min_all", Bundle(*css, filters="cssmin", output="gen/styles.min.css")
        )


@app.route("/w/<job_id>")
@app.route("/widget/<job_id>")
def widget(job_id):
    if not _is_enabled(job_id):
        abort(404)
    x = request.args.get("x", 3)
    widgets = _enabled_jobs()
    # Use the widget matching the job implementation, or an explicitly declared
    # widget
    job = _config()["JOBS"][job_id]
    widget = job.get("job_impl", job_id)
    widget = job.get("widget", widget)
    return render_template(
        "index.html",
        layout="layout_single.html",
        widget=widget,
        job=job_id,
        x=x,
        widgets=widgets,
    )


@app.route("/widget/<widget>/<filename>")
def widget_files(widget, filename):
    public_path = os.path.join(app.widgets_path, widget, "public")
    return send_from_directory(public_path, filename)


@app.route("/")
@app.route("/d/<layout>")
@app.route("/dashboard/<layout>")
def dashboard(layout=None):
    locale = request.args.get("locale")
    widgets = _enabled_jobs()
    layout = layout or _config().get("DEFAULT_LAYOUT")
    if layout is None:
        return render_template("index.html", locale=locale, widgets=widgets)
    try:
        return render_template(
            "index.html",
            layout="layouts/{0}.html".format(layout),
            locale=locale,
            widgets=widgets,
        )
    except TemplateNotFound:
        abort(404)


@app.route("/widgets")
def widgets():
    return jsonify(_enabled_jobs())


@app.route("/events")
def events():
    remote_port = request.environ["REMOTE_PORT"]
    current_queue = queue.Queue()
    app.queues[remote_port] = current_queue

    for event in app.last_events.values():
        current_queue.put(event)

    def consume():
        while True:
            data = current_queue.get()
            if data is None:
                break
            yield "data: %s\n\n" % (data,)

    response = Response(consume(), mimetype="text/event-stream")
    response.headers["X-Accel-Buffering"] = "no"
    return response


@app.route("/events/<job_id>", methods=["POST"])
def create_event(job_id):
    if not _is_enabled(job_id):
        abort(404)
    body = request.get_json()
    if not body:
        abort(400)
    _add_event(job_id, body)
    return "", 201


def _config():
    if app.testing:  # tests set their own config
        return app.config
    app.config.from_envvar("JARVIS_SETTINGS")
    return app.config


def _enabled_jobs():
    config = _config()["JOBS"]
    return [job_id for job_id in config.keys() if config[job_id].get("enabled")]


def _is_enabled(job_id):
    return job_id in _enabled_jobs()


@app.context_processor
def _inject_template_methods():
    return dict(is_job_enabled=_is_enabled)


@app.after_request
def _set_security_headers(response):
    csp = (
        "default-src 'none'; "
        "connect-src 'self'; "
        "img-src 'self' https://i.scdn.co; "
        "script-src 'self' https://cdnjs.cloudflare.com; "
        "style-src 'self' https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
        "font-src https://fonts.gstatic.com"
    )
    response.headers["Content-Security-Policy"] = csp
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


def _schedule_jobs(app):
    offset = 0
    jobs = load_jobs()

    for job_id, job_config in _config()["JOBS"].items():
        job_impl = job_config.get("job_impl", job_id)
        if not job_config.get("enabled"):
            app.logger.info("Skipping disabled job: %s", job_id)
            continue
        if job_impl not in jobs:
            app.logger.info(
                ("Skipping job with ID %s (no such " "implementation: %s)"),
                job_id,
                job_impl,
            )
            continue
        job = jobs[job_impl](job_config)
        if app.debug:
            start_date = datetime.now() + timedelta(seconds=1)
        else:
            offset += randint(4, 10)
            start_date = datetime.now() + timedelta(seconds=offset)

        job.start_date = start_date
        app.logger.info(
            "Scheduling job with ID %s (implementation: %s): %s", job_id, job_impl, job
        )
        app.sched.add_job(
            _run_job,
            "interval",
            name=job_id,
            next_run_time=job.start_date,
            coalesce=True,
            seconds=job.interval,
            kwargs={"job_id": job_id, "job": job},
        )
    if not app.sched.running:
        app.sched.start()


def _add_event(job_id, data):
    json_data = json.dumps(
        {"body": data, "job": job_id}, separators=(",", ":"), sort_keys=True
    )
    app.last_events[job_id] = json_data
    for q in app.queues.values():
        q.put(json_data)


def _run_job(job_id, job):
    try:
        data = job.get()
        _add_event(job_id, data)
    except Exception as e:
        msg = "Failed to execute job: " + job_id + ": " + str(e)
        if app.debug:
            app.logger.warning(msg, e)
        else:
            # Skip logging stack trace
            app.logger.warning(msg)


def _close_stream(*args, **kwargs):
    remote_port = args[2][1]
    if remote_port in app.queues:
        del app.queues[remote_port]


socketserver.BaseServer.handle_error = _close_stream
