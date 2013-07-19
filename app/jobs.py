#!/usr/bin/env python

import dateutil.parser
import httplib2
import imaplib
import os
import re
import requests
from abc import ABCMeta, abstractmethod
from apiclient.discovery import build
from datetime import datetime
from httplib import BadStatusLine
from lxml import etree
from oauth2client.file import Storage
from pyquery import PyQuery as pq
from soco import SoCo
from subprocess import Popen, PIPE


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
            departureTime = dateutil.parser.parse(
                departure['registeredDepartureTime'].split('T').pop())
            remaining = int((departureTime - now).total_seconds() / 60)
            departure['hour'] = departureTime.strftime('%H')
            departure['minute'] = departureTime.strftime('%M')
            departure['eta'] = remaining if remaining > 0 else 0
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
                  d.find('td.title a')
                  .not_('a[href="news2"]')
                  .not_('a[href^="item"]')]
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


class Uptime(AbstractJob):

    def __init__(self, conf):
        self.hosts = conf['hosts']
        self.interval = conf['interval']

    def get(self):
        for host in self.hosts:
            ping_cmd = 'ping6' if ':' in host['ip'] else 'ping'
            ping = '%s -c 1 %s' % (ping_cmd, host['ip'])
            p = Popen(ping.split(' '), stdout=PIPE, stderr=PIPE)
            host['active'] = p.wait() == 0
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

        date = list(d.find('th.date')[0].itertext())[-1]
        departure_times = [el.text_content().strip() for el in
                           d.find('td.depart strong')]
        arrival_times = [el.text_content().strip() for el in
                         d.find('td.arrive strong')]
        durations = [int(el.text_content().rstrip(' min')) for el in
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


class Ping(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']
        self.hosts = conf['hosts']

    def _parse_time(self, ping_output):
        time = re.search('time=(\d+(?:\.\d+)?)', ping_output)
        return float(time.group(1)) if time is not None else 0

    def _get_latency(self, host):
        ping_cmd = 'ping6' if ':' in host[1] else 'ping'
        ping = '%s -c 1 %s' % (ping_cmd, host[1])
        p = Popen(ping.split(' '), stdout=PIPE, stderr=PIPE)
        return self._parse_time(p.communicate()[0])

    def get(self):
        data = {'values': {}}
        for host in self.hosts:
            data['values'][host[0]] = self._get_latency(host)
        return data


class Gmail(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']
        self.email = conf['email']
        self.password = conf['password']
        self.folder = conf['folder']
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)

    def _parse_count(self, message):
        count = re.search('\w+ (\d+)', message)
        return int(count.group(1)) if count is not None else 0

    def _get_count(self):
        _, message = self.mail.status(self.folder, '(MESSAGES)')
        return self._parse_count(message[0])

    def _get_unread_count(self):
        _, message = self.mail.status(self.folder, '(UNSEEN)')
        return self._parse_count(message[0])

    def get(self):
        if self.mail.state == 'NONAUTH':
            self.mail.login(self.email, self.password)
        return {
            'email': self.email,
            'folder': self.folder,
            'count': self._get_count(),
            'unread_count': self._get_unread_count()
        }


def find_cls(name):
    classes = [cls for cls in AbstractJob.__subclasses__()
               if cls.__name__.lower() == name.lower()]
    return classes.pop() if len(classes) > 0 else None


if __name__ == '__main__':
    import sys
    from flask import Flask
    from pprint import pprint

    app = Flask(__name__)
    app.config.from_envvar('JARVIS_SETTINGS')
    conf = app.config['JOBS']

    if len(sys.argv) > 1:
        name = sys.argv[1].lower()
    else:
        jobs = ' '.join([cls.__name__.lower() for cls in
                         AbstractJob.__subclasses__()])
        name = raw_input('Name of the job to run [%s]: ' % (jobs,)).lower()

    cls = find_cls(name)
    if cls is None:
        print 'No such job: %s' % (name,)
        sys.exit(1)

    job = cls(conf[name])
    pprint(job.get())
