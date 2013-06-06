#!/usr/bin/env python

import sys
import os
import yaml
import inspect
import schedule
import Queue
import workers
from flask import Flask, render_template, make_response, Response, \
    stream_with_context, request


app = Flask(__name__)
queued_events = {}


@app.route('/')
def index():
    """Render index template"""
    return render_template('index.html')


@app.route('/styles.css')
def css():
    """Render widget styles"""
    response = make_response(render_template('styles.css'))
    response.headers['Content-Type'] = 'text/css'
    return response


@app.route('/events')
def events():
    remote_port = request.environ['REMOTE_PORT']
    current_queue = Queue.Queue()
    queued_events[remote_port] = current_queue

    def schedule_and_consume():
        while True:
            schedule.run_pending()
            if not current_queue.empty():
                data = current_queue.get(block=False)
                yield 'data: %s\n\n' % (data,)

    return Response(stream_with_context(schedule_and_consume()),
                    mimetype='text/event-stream')


def _read_conf():
    with open(os.path.join(sys.path[0], 'config.yml'), 'r') as conf:
        return yaml.load(conf)


def _configure_jobs(conf):
    for cls_name, cls in inspect.getmembers(workers, inspect.isclass):
        name = cls_name.lower()
        if name not in conf.keys() or not conf[name]['enabled']:
            print 'Skipping missing or disabled worker: %s' % (name,)
            continue
        job = cls(conf)
        print 'Configuring worker %s to run every %d seconds' % (name,
                                                                 job.every)
        schedule.every(job.every).seconds.do(_queue_data, name, job)


def _queue_data(widget, job):
    data = job.get()
    for queue in queued_events.values():
        queue.put(data)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        app.debug = True
    _configure_jobs(_read_conf())
    port = int(os.environ.get('PORT', 5000))
    try:
        app.run(host='0.0.0.0', port=port, threaded=True)
    finally:
        schedule.clear()
