# -*- coding: utf-8 -*-

import os
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from datetime import datetime
from jobs import AbstractJob


class Calendar(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']
        self.timeout = conf.get('timeout')

    def _auth(self):
        credentials_file = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '.calendar.json'))
        storage = Storage(credentials_file)
        credentials = storage.get()
        http = httplib2.Http(timeout=self.timeout)
        http = credentials.authorize(http)
        self.service = build(serviceName='calendar', version='v3', http=http)

    def _parse(self, items):
        events = []
        for item in items:
            date = item['start'].get('dateTime') or item['start'].get('date')
            events.append({
                'id': item['id'],
                'summary': item['summary'],
                'date': date
            })
        return events

    def get(self):
        if not hasattr(self, 'service'):
            self._auth()

        now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        result = self.service.events().list(calendarId='primary',
                                            orderBy='startTime',
                                            singleEvents=True,
                                            timeMin=now).execute()
        return {'events': self._parse(result['items'])}
