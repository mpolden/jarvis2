# -*- coding: utf-8 -*-

import os

import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage

from jobs import AbstractJob


class Gmail(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']
        self.email = conf['email']
        self.folder = conf['folder']
        self.timeout = conf.get('timeout')

    def _auth(self):
        credentials_file = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '.gmail.json'))
        storage = Storage(credentials_file)
        credentials = storage.get()
        http = httplib2.Http(timeout=self.timeout)
        http = credentials.authorize(http)
        self.service = build(serviceName='gmail', version='v1', http=http)

    def _get_count(self):
        result = self.service.users().messages().list(
            userId=self.email, q='label:{}'.format(self.folder)).execute()
        return result.get('resultSizeEstimate', 0)

    def _get_unread_count(self):
        result = self.service.users().messages().list(
            userId=self.email, q='is:unread').execute()
        return result.get('resultSizeEstimate', 0)

    def get(self):
        if not hasattr(self, 'service'):
            self._auth()
        count = self._get_count()
        unread = self._get_unread_count()
        return {
            'email': self.email,
            'folder': self.folder,
            'count': count,
            'unread': unread
        }
