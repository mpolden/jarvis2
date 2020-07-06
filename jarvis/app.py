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
from flask import Flask, render_template, Response, request, abort
from flask_assets import Environment, Bundle
from flask.templating import TemplateNotFound
from jobs import load_jobs
from random import randint


app = Flask(__name__)
app.logger.setLevel(logging.INFO)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
sched = BackgroundScheduler(logger=app.logger)
queues = {}
last_events = {}


@app.before_first_request
def _configure_bundles():
    js = ['main.js']
    css = ['main.css']
    widgets_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                'static', 'widgets'))

    for widget in os.listdir(widgets_path):
        widget_path = os.path.join('widgets', widget)
        for asset_file in os.listdir(os.path.join(widgets_path, widget)):
            asset_path = os.path.join(widget_path, asset_file)
            if asset_file.endswith('.js'):
                js.append(asset_path)
            elif asset_file.endswith('.css'):
                css.append(asset_path)

    assets = Environment(app)
    if app.debug:
        assets.register('js_all', Bundle(*js, output='gen/app.js'))
        assets.register('css_all', Bundle(*css, output='gen/styles.css'))
    else:
        assets.register('js_min_all', Bundle(*js, filters='rjsmin',
                                             output='gen/app.min.js'))
        assets.register('css_min_all', Bundle(*css, filters='cssmin',
                                              output='gen/styles.min.css'))


@app.route('/w/<job_id>')
@app.route('/widget/<job_id>')
def widget(job_id):
    if not _is_enabled(job_id):
        abort(404)
    x = request.args.get('x', 3)
    widgets = _enabled_jobs()
    # Use the widget matching the job implementation, or an explicitly declared
    # widget
    job = _config()['JOBS'][job_id]
    widget = job.get('job_impl', job_id)
    widget = job.get('widget', widget)
    return render_template('index.html', layout='layout_single.html',
                           widget=widget, job=job_id, x=x, widgets=widgets)


@app.route('/')
@app.route('/d/<layout>')
@app.route('/dashboard/<layout>')
def dashboard(layout=None):
    locale = request.args.get('locale')
    widgets = _enabled_jobs()
    layout = layout or _config().get('DEFAULT_LAYOUT')
    if layout is None:
        return render_template('index.html', locale=locale, widgets=widgets)
    try:
        return render_template('index.html',
                               layout='layouts/{0}.html'.format(layout),
                               locale=locale, widgets=widgets)
    except TemplateNotFound:
        abort(404)


@app.route('/events')
def events():
    remote_port = request.environ['REMOTE_PORT']
    current_queue = queue.Queue()
    queues[remote_port] = current_queue

    for event in last_events.values():
        current_queue.put(event)

    def consume():
        while True:
            data = current_queue.get()
            if data is None:
                break
            yield 'data: %s\n\n' % (data,)

    response = Response(consume(), mimetype='text/event-stream')
    response.headers['X-Accel-Buffering'] = 'no'
    return response


@app.route('/events/<job_id>', methods=['POST'])
def create_event(job_id):
    if not _is_enabled(job_id):
        abort(404)
    body = request.get_json()
    if not body:
        abort(400)
    _add_event(job_id, body)
    return '', 201


def _config():
    if app.testing:  # tests set their own config
        return app.config
    app.config.from_envvar('JARVIS_SETTINGS')
    return app.config


def _enabled_jobs():
    config = _config()['JOBS']
    return [job_id for job_id in config.keys()
            if config[job_id].get('enabled')]


def _is_enabled(job_id):
    return job_id in _enabled_jobs()


@app.context_processor
def _inject_template_methods():
    return dict(is_job_enabled=_is_enabled)


@app.before_first_request
def _schedule_jobs():
    offset = 0
    jobs = load_jobs()

    for job_id, job_config in _config()['JOBS'].items():
        job_impl = job_config.get('job_impl', job_id)
        if not job_config.get('enabled'):
            app.logger.info('Skipping disabled job: %s', job_id)
            continue
        if job_impl not in jobs:
            app.logger.info(('Skipping job with ID %s (no such '
                             'implementation: %s)'), job_id, job_impl)
            continue
        job = jobs[job_impl](job_config)
        if app.debug:
            start_date = datetime.now() + timedelta(seconds=1)
        else:
            offset += randint(4, 10)
            start_date = datetime.now() + timedelta(seconds=offset)

        job.start_date = start_date
        app.logger.info('Scheduling job with ID %s (implementation: %s): %s',
                        job_id, job_impl, job)
        sched.add_job(_run_job,
                      'interval',
                      name=job_id,
                      next_run_time=job.start_date,
                      coalesce=True,
                      seconds=job.interval,
                      kwargs={'job_id': job_id, 'job': job})
    if not sched.running:
        sched.start()


def _add_event(job_id, data):
    json_data = json.dumps({
        'body': data,
        'job': job_id
    }, separators=(',', ':'), sort_keys=True)
    last_events[job_id] = json_data
    for q in queues.values():
        q.put(json_data)


def _run_job(job_id, job):
    try:
        data = job.get()
        _add_event(job_id, data)
    except Exception:
        app.logger.exception('Failed to execute job with ID: ' + job_id)


def _close_stream(*args, **kwargs):
    remote_port = args[2][1]
    if remote_port in queues:
        del queues[remote_port]


socketserver.BaseServer.handle_error = _close_stream
