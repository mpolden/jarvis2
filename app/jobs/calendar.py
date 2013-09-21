#!/usr/bin/env python

import dateutil.parser
import httplib2
import os
from apiclient.discovery import build
from datetime import datetime
from httplib import BadStatusLine
from jobs import AbstractJob
from oauth2client.file import Storage


class Calendar(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']
        self.api_key = conf['api_key']

    def _auth(self):
        credentials_file = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '.calendar.json'))
        storage = Storage(credentials_file)
        credentials = storage.get()
        http = httplib2.Http()
        http = credentials.authorize(http)
        self.service = build(serviceName='calendar', version='v3', http=http,
                             developerKey=self.api_key)

    def _parse_date(self, date):
        if 'dateTime' in date:
            d = date['dateTime']
        elif 'date' in date:
            d = date['date']
        else:
            return None
        return dateutil.parser.parse(d)

    def _parse(self, items):
        events = []
        for item in items:
            date = self._parse_date(item['start'])
            events.append({
                'id': item['id'],
                'summary': item['summary'],
                'date': date.strftime('%Y-%m-%d %H:%M:%S')
            })
        return events

    def get(self):
        if not hasattr(self, 'service'):
            self._auth()

        now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        try:
            result = self.service.events().list(calendarId='primary',
                                                orderBy='startTime',
                                                singleEvents=True,
                                                timeMin=now).execute()
        except BadStatusLine:
            return {}

        return {'events': self._parse(result['items'])}
