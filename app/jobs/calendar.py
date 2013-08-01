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

    def get_current_event(self, items):
        if len(items) == 0:
            return None

        event = None
        for item in items:
            date = self._parse_date(item['start'])
            if date is None:
                continue
            today = date.now().date()
            if date.date() == today:
                event = (item, date)
                break
            elif date.date() < today:
                event = (item, date)

        if event is None:
            return None

        return {
            'id': event[0]['id'],
            'summary': event[0]['summary'],
            'start': event[1].strftime('%H:%M')
        }

    def get_events(self, items, today):
        if len(items) == 0:
            return None

        events = []
        for item in items:
            if today is not None and today['id'] == item['id']:
                continue
            date = self._parse_date(item['start'])
            events.append({
                'id': item['id'],
                'summary': item['summary'],
                'start': date.strftime('%d.%m %H:%M')
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

        items = result['items']
        today = self.get_current_event(items)
        events = self.get_events(items, today)
        return {
            'today': today,
            'events': events
        }
