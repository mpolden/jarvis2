#!/usr/bin/env python

import jobs
import json
import os
import Queue
import SocketServer
from apscheduler.scheduler import Scheduler
from datetime import datetime, timedelta
from flask import Flask, render_template, Response, request, abort, url_for
from flask.ext.assets import Environment, Bundle
from random import randint


app = Flask(__name__)
app.config.from_envvar('JARVIS_SETTINGS')
assets = Environment(app)
sched = Scheduler()
queues = {}
last_events = {}


@app.before_first_request
def _configure_bundles():
    js_vendor = [
        'js/jquery/jquery.min.js',
        'js/gridster/jquery.gridster.min.js',
        'js/jquery-knob/jquery.knob.min.js',
        'js/angular/angular.min.js',
        'js/angular-truncate/angular-truncate.min.js',
        'js/d3/d3.min.js',
        'js/rickshaw/rickshaw.min.js',
        'js/moment/moment.min.js'
    ]
    js = [
        'js/app/gridster.js',
        'js/app/main.js'
    ]
    css_vendor = [
        'css/normalize-css/normalize.css',
        'css/gridster/jquery.gridster.css',
        'css/rickshaw/rickshaw.css'
    ]
    css = [
        'css/app/styles.css'
    ]

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

    assets.register('js_all', Bundle(*(js_vendor + js),
                                     output='assets/app.js'))
    assets.register('css_all', Bundle(*(css_vendor + css),
                                      output='assets/styles.css'))
    assets.register('js_min_all', Bundle(Bundle(*js_vendor),
                                         Bundle(*js, filters='rjsmin'),
                                         output='assets/app.min.js'))
    assets.register('css_min_all', Bundle(*(css_vendor + css),
                                          filters='cssmin',
                                          output='assets/styles.min.css'))


@app.route('/')
@app.route('/<widget>')
def index(widget=None):
    if widget is not None:
        if not _is_enabled(widget):
            abort(404)
        x = request.args.get('x', 2)
        y = request.args.get('y', 2)
        return render_template('index.html', layout='layout_single.html',
                               widget=widget, x=x, y=y)
    return render_template('index.html')


@app.route('/events')
def events():
    remote_port = request.environ['REMOTE_PORT']
    current_queue = Queue.Queue()
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


def _is_enabled(name, conf=None):
    if conf is None:
        conf = app.config['JOBS']
    return name in conf and conf[name].get('enabled')


@app.context_processor
def _inject_template_methods():
    def url_for_mtime(endpoint, **values):
        if endpoint == 'static':
            filename = values.get('filename', None)
            if filename is not None:
                file_path = os.path.join(app.root_path, endpoint, filename)
                values['t'] = int(os.stat(file_path).st_mtime)
        return url_for(endpoint, **values)
    return dict(url_for_mtime=url_for_mtime, is_widget_enabled=_is_enabled)


@app.before_first_request
def _configure_jobs():
    conf = app.config['JOBS']
    offset = 0
    for cls in jobs.AbstractJob.__subclasses__():
        name = cls.__name__.lower()
        if not _is_enabled(name, conf):
            print 'Skipping disabled job: %s' % (name,)
            continue
        job = cls(conf[name])
        if app.debug:
            start_date = datetime.now() + timedelta(seconds=1)
        else:
            offset += randint(4, 10)
            start_date = datetime.now() + timedelta(seconds=offset)
        print 'Configuring job: %s [start_date=%s, seconds=%s]' % \
            (name, start_date, job.interval)
        sched.add_interval_job(_run_job,
                               seconds=job.interval,
                               start_date=start_date,
                               kwargs={'widget': name, 'job': job})
    if not sched.running:
        sched.start()


def _run_job(widget, job):
    body = job.get()
    if not body:
        return
    body['updated_at'] = datetime.now().strftime('%H:%M')
    json_data = json.dumps({
        'widget': widget,
        'body': body
    })
    last_events[widget] = json_data
    for queue in queues.values():
        queue.put(json_data)


def _close_stream(*args, **kwargs):
    remote_port = args[2][1]
    if remote_port in queues:
        del queues[remote_port]


SocketServer.BaseServer.handle_error = _close_stream
