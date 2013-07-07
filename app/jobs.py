#!/usr/bin/env python

import dateutil.parser
import httplib2
import os
import requests
from abc import ABCMeta, abstractmethod
from apiclient.discovery import build
from datetime import datetime
from lxml import etree
from oauth2client.file import Storage
from pyquery import PyQuery as pq
from soco import SoCo
from subprocess import call


class AbstractJob(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self):
        return


class Yr(AbstractJob):

    def __init__(self, conf):
        self.url = conf['url']
        self.interval = conf['interval']

    def _parse(self, xml):
        tree = etree.fromstring(xml)
        tabular = tree.xpath('/weatherdata/forecast/tabular/time[1]').pop()
        weatherStation = tree.xpath(
            '/weatherdata/observations/weatherstation[1]').pop()
        windSpeed = weatherStation.xpath('windSpeed').pop()
        return {
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

    def get(self):
        r = requests.get(self.url)

        if r.status_code == 200 and len(r.content) > 0:
            return self._parse(r.content)
        return {}


class Atb(AbstractJob):

    def __init__(self, conf):
        self.url = conf['url']
        self.interval = conf['interval']

    def _parse(self, data, now=None):
        if now is None:
            now = datetime.now()
        for departure in data['departures']:
            departureTime = datetime.strptime(
                departure['registeredDepartureTime'],
                '%Y-%m-%dT%H:%M:%S.000')
            remaining = (departureTime - now).total_seconds() / 60
            departure['hour'] = departureTime.strftime('%H')
            departure['minute'] = departureTime.strftime('%M')
            if remaining > 0:
                departure['eta'] = int(remaining)
            else:
                departure['eta'] = 0
        return data

    def get(self):
        r = requests.get(self.url)

        if r.status_code == 200 and len(r.content) > 0:
            return self._parse(r.json())
        return {}


class HackerNews(AbstractJob):

    def __init__(self, conf):
        self.url = 'https://news.ycombinator.com'
        self.interval = conf['interval']

    def _parse(self, html):
        d = pq(html)

        titles = [el.text for el in
                  d.find('td.title a').not_('a[href="news2"]')]
        points = [int(el.text.rstrip(' points')) for el in
                  d.find('td.subtext span')]

        items = []
        for title, num_points in zip(titles, points):
            items.append({
                'title': title,
                'points': num_points
            })

        return {'items': items}

    def get(self):
        r = requests.get(self.url)

        if r.status_code == 200 and len(r.content) > 0:
            return self._parse(r.content)
        return {}


class Sonos(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']
        self.sonos = SoCo(conf['ip'])

    def get(self):
        try:
            current_track = self.sonos.get_current_track_info()
            next_track = self.sonos.get_queue(
                int(current_track['playlist_position']), 1).pop()
            return {
                'room': self.sonos.get_speaker_info()['zone_name'],
                'current': current_track,
                'next': next_track
            }
        except:
            return {}


class Calendar(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']

        credentials_file = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '.calendar.json'))
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


class Uptime(AbstractJob):

    def __init__(self, conf):
        self.hosts = conf['hosts']
        self.interval = conf['interval']

    def get(self):
        with open(os.devnull, 'w') as devnull:
            for host in self.hosts:
                ping = 'ping -c 1 -t 1 -q %s' % (host['ip'],)
                up = call(ping.split(' '), stdout=devnull, stderr=devnull)
                host['active'] = (up == 0)
        return {'hosts': self.hosts}


class Plex(AbstractJob):

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


class Nsb(AbstractJob):

    def __init__(self, conf):
        self.from_location = conf['from']
        self.to_location = conf['to']
        self.url = ('https://www.nsb.no/category2734.html'
                    '?booking-from=%s'
                    '&booking-to=%s'
                    '&booking-type=single'
                    '&booking-date=%s'
                    '&booking-date_outward_hour=%s')
        self.interval = conf['interval']

    def _parse(self, html):
        d = pq(html)

        date = d.find('th.date').pop().text_content().lstrip('Spor')
        departure_times = [el.text_content().strip() for el in
                           d.find('td.depart strong')]
        arrival_times = [el.text_content().strip() for el in
                         d.find('td.arrive strong')]
        durations = [el.text_content().rstrip(' min') for el in
                     d.find('td.duration em')]

        departures = []
        for departure, arrival, duration in zip(departure_times, arrival_times,
                                                durations):
            departures.append({
                'departure': departure,
                'arrival': arrival,
                'duration': duration
            })

        return {
            'date': date.partition(', ')[2],
            'from': self.from_location,
            'to': self.to_location,
            'departures': departures
        }

    def get(self):
        now = datetime.now()
        params = (self.from_location, self.to_location,
                  now.strftime('%d-%m-%Y'), now.strftime('%H'))
        r = requests.get(self.url % params)

        if r.status_code == 200 and len(r.content) > 0:
            return self._parse(r.content)
        return {}
