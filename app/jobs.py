#!/usr/bin/env python

import requests
import json
import os
import dateutil.parser
from subprocess import call
from datetime import datetime
from lxml import etree
from soco import SoCo

import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage


class Base(object):

    def get(self):
        raise NotImplementedError('Needs to be implemented')


class Yr(Base):

    def __init__(self, conf):
        self.url = conf['url']
        self.interval = conf['interval']

    def get(self):
        # Retrieve XML data from YR_URL
        r = requests.get(self.url)

        # Parse XML string into an ElementTree
        tree = etree.fromstring(r.content)

        # Use XPath to get the values we're interested in
        tabular = tree.xpath('/weatherdata/forecast/tabular/time[1]').pop()
        weatherStation = tree.xpath(
            '/weatherdata/observations/weatherstation[1]').pop()
        windSpeed = weatherStation.xpath('windSpeed').pop()
        data = {
            'location': tree.xpath('/weatherdata/location/name').pop().text,
            'temperature': weatherStation.xpath('temperature').pop().get(
                'value'),
            'description': tabular.xpath('symbol').pop().get('name'),
            'wind': {
                'speed': windSpeed.get('mps'),
                'description': windSpeed.get('name'),
                'direction': weatherStation.xpath('windDirection').pop().get(
                    'name')
            }
        }
        return data


class Atb(Base):

    def __init__(self, conf):
        self.url = conf['url']
        self.interval = conf['interval']

    def get(self):
        r = requests.get(self.url)

        if r.status_code == 200 and len(r.content) > 0:
            data = json.loads(r.content)
            for departure in data['departures']:
                departureTime = datetime.strptime(
                    departure['registeredDepartureTime'],
                    '%Y-%m-%dT%H:%M:%S.000')
                remaining = (departureTime - datetime.now()
                             ).total_seconds() / 60
                departure['hour'] = departureTime.strftime('%H')
                departure['minute'] = departureTime.strftime('%M')
                if remaining > 0:
                    departure['remaining'] = int(remaining)
                else:
                    departure['remaining'] = 0

            return data
        return {}


class HackerNews(Base):

    def __init__(self, conf):
        self.url = conf['url']
        self.interval = conf['interval']

    def get(self):
        r = requests.get(self.url)

        if r.status_code == 200 and len(r.content) > 0:
            return json.loads(r.content)
        return {}


class Sonos(Base):

    def __init__(self, conf):
        self.ip = conf['ip']
        self.interval = conf['interval']

    def get(self):
        sonos = SoCo(self.ip)

        np = sonos.get_current_track_info()
        next = sonos.get_queue(int(np['playlist_position']), 1).pop()
        return {
            'name': sonos.get_speaker_info()['zone_name'],
            'np': np,
            'next': next
        }


class Calendar(Base):

    def __init__(self, conf):
        self.interval = conf['interval']

        credentials_file = os.path.join(os.path.dirname(__file__),
                                        '.calendar.json')
        storage = Storage(credentials_file)
        credentials = storage.get()
        http = httplib2.Http()
        http = credentials.authorize(http)
        self.service = build(serviceName='calendar', version='v3', http=http,
                             developerKey=conf['api_key'])

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

        event = items[0]
        date = self._parse_date(event['start'])

        if date is None or date.date() != date.now().date():
            return None

        return {
            'summary': event['summary'],
            'start': date.strftime('%H:%M')
        }

    def get_events(self, items, today):
        if len(items) == 0:
            return None

        events = []
        start = 0 if today is None else 1
        for event in items[start:]:
            date = self._parse_date(event['start'])
            events.append({
                'summary': event['summary'],
                'start': date.strftime('%d.%m %H:%M')
            })
        return events

    def get(self):
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        result = self.service.events().list(calendarId='primary',
                                            orderBy='startTime',
                                            singleEvents=True,
                                            timeMin=now).execute()
        items = result['items']
        today = self.get_current_event(items)
        events = self.get_events(items, today)
        return {
            'today': today,
            'events': events
        }


class Uptime(Base):

    def __init__(self, conf):
        self.hosts = conf['hosts']
        self.interval = conf['interval']

    def get(self):
        with open(os.devnull, 'w') as devnull:
            for host in self.hosts:
                ping = 'ping -c 1 -t 1 -q %s' % (host['ip'],)
                up = call(ping.split(' '), stdout=devnull, stderr=devnull)
                host['active'] = (up == 0)
        return self.hosts


class Plex(Base):

    def __init__(self, conf):
        self.interval = conf['interval']
        self.movies = conf['movies']
        self.shows = conf['shows']

    def get(self):
        r = requests.get(self.movies)
        movies_doc = etree.fromstring(r.content)

        r = requests.get(self.shows)
        shows_doc = etree.fromstring(r.content)

        data = {
            'movies': [],
            'shows': []
        }
        for movie in movies_doc.xpath('/MediaContainer/Video'):
            data['movies'].append({
                'title': movie.get('title'),
                'year': movie.get('year')
            })
        for show in shows_doc.xpath('/MediaContainer/Video'):
            data['shows'].append({
                'name': show.get('grandparentTitle'),
                'title': show.get('title'),
                'episode': show.get('index').zfill(2),
                'season': show.get('parentIndex').zfill(2)
            })
        return data
