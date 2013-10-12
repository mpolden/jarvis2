#!/usr/bin/env python

"""JARVIS 2 helper script

Usage:
  run.py -j [-n <job>] [-s]
  run.py [-d]

Options:
  -h --help         Show usage
  -d --debug        Run app in debug mode
  -j --job          Run a job
  -n --name=JOB     Name of job to run, will prompt if omitted
  -s --json         Print job output as JSON

"""
from __future__ import print_function

import os
import signal

from docopt import docopt

from main import app, queues, sched


def _teardown(signal, frame):
    sched.shutdown(wait=False)
    for queue in queues.values():
        queue.put(None)
    queues.clear()
    # Let the interrupt bubble up so that Flask/Werkzeug see it
    raise KeyboardInterrupt


def _run_job(name=None, print_json=False):
    import json
    import sys
    from flask import Flask
    from jobs import load_jobs
    from pprint import pprint

    _app = Flask(__name__)
    _app.config.from_envvar('JARVIS_SETTINGS')
    conf = _app.config['JOBS']

    jobs = load_jobs()
    if name is None or len(name) == 0:
        names = ' '.join(jobs.keys())
        name = raw_input('Name of the job to run [%s]: ' % (names,)).lower()

    cls = jobs.get(name)
    if cls is None:
        print('No such job: %s' % (name,))
        sys.exit(1)

    job = cls(conf[name])
    data = job.get()
    if print_json:
        print(json.dumps(data, indent=2))
    else:
        pprint(data)


def _run_app(debug=False):
    app.debug = debug
    signal.signal(signal.SIGINT, _teardown)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, use_reloader=False, threaded=True)


def main():
    args = docopt(__doc__)
    if args['--job']:
        _run_job(args['--name'], args['--json'])
    else:
        _run_app(args['--debug'])


if __name__ == '__main__':
    main()
