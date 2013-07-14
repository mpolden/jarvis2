#!/usr/bin/env python

import logging
import os
import signal
import sys
from app.main import app, queues, sched


def _teardown(signal, frame):
    sched.shutdown(wait=False)
    for queue in queues.values():
        queue.put(None)
    queues.clear()
    # Let the interrupt bubble up so that Flask/Werkzeug see it
    raise KeyboardInterrupt


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        logging.basicConfig()
        app.debug = True
    signal.signal(signal.SIGINT, _teardown)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, use_reloader=False, threaded=True)
