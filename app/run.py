#!/usr/bin/env python

from __future__ import print_function

import argparse
import os
import signal

try:
    # Python 2
    input = raw_input
except NameError:
    pass

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
    from jobs import load_jobs
    from pprint import pprint

    jobs = load_jobs()
    if name is None or len(name) == 0:
        names = ' '.join(jobs.keys())
        name = input('Name of the job to run [%s]: ' % (names,)).lower()

    cls = jobs.get(name)
    if cls is None:
        print('No such job: %s' % (name,))
        sys.exit(1)

    job_conf = app.config['JOBS'].get(name)
    if job_conf is None:
        print('No config found for job: %s' % (name,))
        sys.exit(1)

    job = cls(job_conf)
    data = job.get()
    if print_json:
        print(json.dumps(data, indent=2))
    else:
        pprint(data)


def _run_app(debug=False):
    app.jinja_env.auto_reload = debug
    app.debug = debug
    signal.signal(signal.SIGINT, _teardown)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, use_reloader=False, threaded=True)


def main():
    parser = argparse.ArgumentParser(description='Helper script.')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true',
                        help='Run app in debug mode')
    parser.add_argument('-j', '--job', dest='job', action='store_true',
                        help='Run a job, will prompt if NAME is not given')
    parser.add_argument('-s', '--json', dest='json', action='store_true',
                        help='Print job output as JSON')
    parser.add_argument('name', metavar='NAME', nargs='?')
    args = parser.parse_args()

    if args.job:
        _run_job(args.name, args.json)
    else:
        _run_app(args.debug)


if __name__ == '__main__':
    main()
