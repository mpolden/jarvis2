#!/usr/bin/env python

from __future__ import print_function
import os
import signal
import sys
from main import app, queues, sched


def _teardown(signal, frame):
    sched.shutdown(wait=False)
    for queue in queues.values():
        queue.put(None)
    queues.clear()
    # Let the interrupt bubble up so that Flask/Werkzeug see it
    raise KeyboardInterrupt


def _run_job(name=None):
    import json
    import sys
    from flask import Flask
    from jobs import load_jobs
    from pprint import pprint

    app = Flask(__name__)
    app.config.from_envvar('JARVIS_SETTINGS')
    conf = app.config['JOBS']

    jobs = load_jobs()
    if name is None:
        names = ' '.join(jobs.keys())
        name = raw_input('Name of the job to run [%s]: ' % (names,)).lower()

    print_json = name.endswith('.json')
    if print_json:
        name = name.rstrip('.json')

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

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'debug':
            app.debug = True
        elif sys.argv[1] == 'job':
            _run_job(sys.argv[2] if len(sys.argv) > 2 else None)
            sys.exit(0)
    signal.signal(signal.SIGINT, _teardown)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, use_reloader=False, threaded=True)
