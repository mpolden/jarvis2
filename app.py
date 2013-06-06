#!/usr/bin/env python

import sys
import os
import yaml
import inspect
from flask import Flask, render_template, make_response, Response, \
    stream_with_context

import workers

app = Flask(__name__)
active_workers = []


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
    def generate():
        for worker in active_workers:
            yield 'data: %s\n\n' % (worker.get(),)
    return Response(stream_with_context(generate()),
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
        print 'Configuring worker: %s' % (name,)
        worker = cls(conf)
        active_workers.append(worker)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        app.debug = True
    _configure_jobs(_read_conf())
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)
