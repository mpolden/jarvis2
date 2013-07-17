#!/usr/bin/env python

import sys
import os.path

from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from flask import Flask

app = Flask(__name__)
app.config.from_envvar('JARVIS_SETTINGS')
config = app.config['JOBS']['calendar']


def main():
    if 'client_id' not in config \
            or 'client_secret' not in config \
            or 'api_key' not in config:
        print ('Error: client_id, client_secret or api_key is not set.\n\n'
               'Please create a client ID and server key here and update '
               'config.py:\n\nhttps://code.google.com/apis/console/#:access')
        sys.exit(1)

    FLOW = OAuth2WebServerFlow(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        scope='https://www.googleapis.com/auth/calendar.readonly')

    credentials_file = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       '.calendar.json'))
    storage = Storage(credentials_file)
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = run(FLOW, storage)
    else:
        print 'Google API credentials already exist: %s' % (credentials_file,)


if __name__ == '__main__':
    main()
