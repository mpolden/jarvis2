#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import sys
import argparse

from flask import Flask
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client import tools


app = Flask(__name__, instance_relative_config=True,
            instance_path=os.path.abspath(os.path.join(
                os.path.dirname(__file__), '..', 'app')))
app.config.from_envvar('JARVIS_SETTINGS')


def get_config(name):
    return app.config['JOBS'][name]


def create_credentials(name):
    config = get_config(name)
    if 'client_id' not in config \
            or 'client_secret' not in config:
        print('Error: client_id, client_secret is not set.\n\n'
              'Please create a client ID here and update '
              'config.py:\n\nhttps://code.google.com/apis/console/#:access')
        sys.exit(1)

    FLOW = OAuth2WebServerFlow(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        scope='https://www.googleapis.com/auth/{}.readonly'.format(name))

    run_flags = tools.argparser.parse_args(args=[])

    credentials_file = os.path.join(app.instance_path, 'jobs',
                                    '.{}.json'.format(name))
    storage = Storage(credentials_file)
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(FLOW, storage, run_flags)
    else:
        print('Google API credentials already exist: %s' % (credentials_file,))


def main():
    parser = argparse.ArgumentParser(
       description='Create Google API credentials.'
    )
    parser.add_argument('name', metavar='NAME', nargs='?')
    args = parser.parse_args()
    name = args.name

    if name is None:
        name = input(('Enter widget to generate credentials for (gmail'
                      ' or calendar): '))

    if name not in ('calendar', 'gmail'):
        print('Name must be either \'gmail\' or \'calendar\'')
        sys.exit(1)

    create_credentials(name)


if __name__ == '__main__':
    main()
