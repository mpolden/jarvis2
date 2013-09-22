#!/usr/bin/env python

from __future__ import print_function
import os.path
import sys
from flask import Flask
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client.tools import run

app = Flask(__name__, instance_relative_config=True,
            instance_path=os.path.abspath(os.path.join(
                os.path.dirname(__file__), '..', 'app')))
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

    credentials_file = os.path.join(app.instance_path, 'jobs',
                                    '.calendar.json')
    storage = Storage(credentials_file)
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = run(FLOW, storage)
    else:
        print('Google API credentials already exist: %s' % (credentials_file,))


if __name__ == '__main__':
    main()
