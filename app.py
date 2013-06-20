#!/usr/bin/env python

import sys
import os
import yaml
import inspect
import Queue
import jobs
import SocketServer
import json
from time import time
from apscheduler.scheduler import Scheduler
from flask import Flask, render_template, Response, stream_with_context, \
    request
from flask.ext.assets import Environment, Bundle


app = Flask(__name__)
assets = Environment(app)
sched = Scheduler()
queued_events = {}
last_events = {}


@app.before_first_request
def _configure_assets():
    """Configure widget assets"""
    js_files = [
            'js/jquery/jquery.min.js',
            'js/gridster/jquery.gridster.min.js',
            'js/angular/angular.min.js',
            'js/gridster.js',
            'js/app.js'
            ]
    css_files = [
            'css/normalize-css/normalize.css',
            'css/gridster/jquery.gridster.min.css',
            'css/styles.css'
            ]
    less_files = ['css/styles.less']
    widgets_path = os.path.join(sys.path[0], 'static', 'widgets')
    for widget in os.listdir(widgets_path):
        widget_path = os.path.join('widgets', widget)
        for asset_file in os.listdir(os.path.join(widgets_path, widget)):
            asset_path = os.path.join(widget_path, asset_file)
            if asset_file.endswith('.js'):
                js_files.append(asset_path)
            elif asset_file.endswith('.less'):
                less_files.append(asset_path)
            elif asset_file.endswith('.css'):
                css_files.append(asset_path)
    js = Bundle(*js_files, filters='jsmin', output='assets/app.min.js')
    less = Bundle(*less_files, output='assets/styles.less')
    css = Bundle(*css_files, filters='cssmin', output='assets/styles.min.css')
    assets.register('js_all', js)
    assets.register('less_all', less)
    assets.register('css_all', css)


@app.route('/')
def index():
    """Render index template"""
    return render_template('index.html')


@app.route('/events')
def events():
    remote_port = request.environ['REMOTE_PORT']
    current_queue = Queue.Queue()
    queued_events[remote_port] = current_queue

    for event in last_events.values():
        current_queue.put(event)

    def consume():
        while True:
            data = current_queue.get()
            yield 'data: %s\n\n' % (data,)

    return Response(stream_with_context(consume()),
                    mimetype='text/event-stream')


def _read_conf():
    with open(os.path.join(sys.path[0], 'config.yml'), 'r') as conf:
        return yaml.load(conf)


@app.before_first_request
def _configure_jobs():
    conf = _read_conf()
    for cls_name, cls in inspect.getmembers(jobs, inspect.isclass):
        name = cls_name.lower()
        if name not in conf.keys() or not conf[name]['enabled']:
            print 'Skipping missing or disabled job: %s' % (name,)
            continue
        job = cls(conf[name])
        print 'Configuring job %s to run every %d seconds' % (name,
                                                              job.interval)
        _queue_data(name, job)
        sched.add_interval_job(_queue_data, seconds=job.interval, kwargs={
            'widget': name, 'job': job})
    if not sched.running:
        sched.start()


def _queue_data(widget, job):
    json_data = json.dumps({
        'widget': widget,
        'timestamp': int(time()),
        'body': job.get()
    })
    last_events[widget] = json_data
    for queue in queued_events.values():
        queue.put(json_data)


def _close_stream(*args, **kwargs):
    remote_port = args[2][1]
    if remote_port in queued_events:
        del queued_events[remote_port]


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        app.debug = True
    port = int(os.environ.get('PORT', 5000))
    SocketServer.BaseServer.handle_error = _close_stream
    try:
        app.run(host='0.0.0.0', port=port, threaded=True)
    finally:
        sched.shutdown(wait=False)
