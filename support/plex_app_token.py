#!/usr/bin/env python

"""Create an Plex App

Usage:
  plex_app_token.py <plex username> <plex password>

Options:
  -h --help         Show usage

"""
from __future__ import print_function

import os.path
import sys
import string
import random
import argparse

import requests
from docopt import docopt
from flask import Flask
from xml.dom import minidom

app = Flask(__name__, instance_relative_config=True,
            instance_path=os.path.abspath(os.path.join(
                os.path.dirname(__file__), '..', 'app')))
app.config.from_envvar('JARVIS_SETTINGS')


def _get_token(username, password):
    rand_ident = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))

    headers = {'X-Plex-Client-Identifier': rand_ident,
               'X-Plex-Device-Name': 'jarvis2',
               'X-Plex-Product': 'jarvis2',
               'X-Plex-Version': '1.0'}
    auth = (username, password)

    s = requests.Session()
    r = s.post('https://plex.tv/users/sign_in.json ', timeout=60, headers=headers, auth=auth)
    dom = minidom.parseString(r.content)

    return dom.getElementsByTagName('user')[0].getAttribute('authenticationToken')


def main():
    config = app.config['JOBS']['plex']['plex_token']

    if config == '':
        username = raw_input('Enter your Plex username: ')
        password = raw_input('Enter your Plex password: ')

        if username is None:
            print('You need to enter a username.')
        if password is None:
            print('You need to enter a password.')

        token = _get_token(username, password)

        print("You're app token is: " + token)
    else:
        print('Plex token already set.')
        sys.exit(1)


if __name__ == '__main__':
    main()
