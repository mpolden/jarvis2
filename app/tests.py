#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os.path
import unittest
from datetime import datetime, timedelta
from jobs import yr, atb, hackernews, nsb, ping, calendar, gmail
from lxml import etree


class Yr(unittest.TestCase):

    def setUp(self):
        xml_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   'test_data',
                                   'varsel.xml'))
        with open(xml_path, 'r') as f:
            self.tree = etree.fromstring(f.read())

    def test_parse_tree(self):
        y = yr.Yr({'interval': None, 'url': None})
        data = y._parse_tree(self.tree)

        self.assertEqual('Delvis skyet', data['description'])
        self.assertEqual('Trondheim', data['location'])
        self.assertEqual('16.3', data['temperature'])
        self.assertEqual('Nord', data['wind']['direction'])
        self.assertEqual('0.7', data['wind']['speed'])
        self.assertEqual('Flau vind', data['wind']['description'])

    def test_parse_tree_date(self):
        y = yr.Yr({'interval': None, 'url': None})
        data = y._parse_tree_date(self.tree, datetime(2013, 7, 1))

        self.assertEqual('Regn', data['description'])
        self.assertEqual('Trondheim', data['location'])
        self.assertEqual('23', data['temperature'])
        self.assertEqual(u'Sør', data['wind']['direction'])
        self.assertEqual('3.6', data['wind']['speed'])
        self.assertEqual('Lett bris', data['wind']['description'])


class Atb(unittest.TestCase):

    def setUp(self):
        json_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                    'test_data',
                                    'atb.json'))
        with open(json_path, 'r') as f:
            self.json = json.loads(f.read())

    def test_parse(self):
        a = atb.Atb({'interval': None, 'url': None})
        now = datetime.now()
        data = a._parse(self.json, now=datetime(now.year, now.month, now.day,
                                                21, 30, 0, 0))

        departures = data['departures']
        self.assertEqual(5, len(departures))
        self.assertEqual(5, departures[0]['eta'])
        self.assertEqual(5, departures[1]['eta'])
        self.assertEqual(5, departures[2]['eta'])
        self.assertEqual(8, departures[3]['eta'])
        self.assertEqual(10, departures[4]['eta'])

    def test_parse_gt_or_eq_zero(self):
        a = atb.Atb({'interval': None, 'url': None})
        now = datetime.now()
        data = a._parse(self.json, now=datetime(now.year, now.month, now.day,
                                                21, 35, 0, 0))

        departures = data['departures']
        self.assertEqual(5, len(departures))
        self.assertEqual(0, departures[0]['eta'])
        self.assertEqual(0, departures[1]['eta'])
        self.assertEqual(0, departures[2]['eta'])
        self.assertEqual(3, departures[3]['eta'])
        self.assertEqual(5, departures[4]['eta'])


class HackerNews(unittest.TestCase):

    def setUp(self):
        html_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                    'test_data',
                                    'hn.html'))
        with open(html_path, 'r') as f:
            self.html = f.read()
        self.hn = hackernews.HackerNews({'interval': None})

    def test_parse(self):
        data = self.hn._parse(self.html)

        self.assertEqual(29, len(data['items']))
        self.assertTrue('points' in data['items'][0])
        self.assertTrue('title' in data['items'][0])
        self.assertEqual(220, data['items'][0]['points'])
        self.assertEqual('Do Things that Don\'t Scale',
                         data['items'][0]['title'])


class Nsb(unittest.TestCase):

    def setUp(self):
        test_data = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                    'test_data'))
        with open(os.path.join(test_data, 'nsb.html')) as f:
            self.html = f.read()

        with open(os.path.join(test_data, 'nsb2.html')) as f:
            self.html2 = f.read()

        self.nsb = nsb.Nsb({'interval': None, 'from': 'Lerkendal',
                            'to': 'Rotvoll'})

    def test_parse(self):
        data = self.nsb._parse(self.html)

        self.assertEqual('15. juli 2013', data['date'])
        self.assertEqual('Rotvoll', data['to'])
        self.assertEqual('Lerkendal', data['from'])
        self.assertEqual(5, len(data['departures']))
        self.assertEqual('06:17', data['departures'][0]['arrival'])
        self.assertEqual('05:56', data['departures'][0]['departure'])
        self.assertEqual(21, data['departures'][0]['duration'])

    def test_parse_multiple_dates(self):
        data = self.nsb._parse(self.html2)

        self.assertEqual('17. juli 2013', data['date'])
        self.assertEqual('Rotvoll', data['to'])
        self.assertEqual('Lerkendal', data['from'])
        self.assertEqual(5, len(data['departures']))
        self.assertEqual('19:17', data['departures'][0]['arrival'])
        self.assertEqual('18:56', data['departures'][0]['departure'])
        self.assertEqual(21, data['departures'][0]['duration'])


class Ping(unittest.TestCase):

    def setUp(self):
        self.ping = ping.Ping({'interval': None, 'hosts': None})

    def test_parse_time(self):
        s = ('PING google.com (173.194.69.139): 56 data bytes\n'
             '64 bytes from 173.194.69.139: icmp_seq=0 ttl=46 time=57.478 ms\n'
             '\n--- google.com ping statistics ---\n'
             '1 packets transmitted, 1 packets received, 0.0% packet loss\n'
             'round-trip min/avg/max/stddev = 57.478/57.478/57.478/0.000 ms\n')

        self.assertEqual(57.478, self.ping._parse_time(s))
        self.assertEqual(0, self.ping._parse_time('foo bar'))


class Calendar(unittest.TestCase):

    def setUp(self):
        self.calendar = calendar.Calendar({'interval': None, 'api_key': None})

    def test_parse_date(self):
        date = datetime(2013, 7, 17)
        dateTime = datetime(2013, 7, 17, 20)

        self.assertEqual(dateTime, self.calendar._parse_date(
            {'dateTime': dateTime.strftime('%Y-%m-%dT%H:%M:%S')}))

        self.assertEqual(date, self.calendar._parse_date(
            {'date': date.strftime('%Y-%m-%d')}))

        self.assertEqual(None, self.calendar._parse_date({}))

    def test_get_current_event_today(self):
        now = datetime.now()
        date1 = now + timedelta(days=1)
        date2 = now + timedelta(days=5)
        date3 = now + timedelta(days=7)
        items = [
            {'id': 1, 'start': {'dateTime': now.strftime('%Y-%m-%dT%H:%M:%S')},
             'summary': 'Event 1'},
            {'id': 2, 'start': {'date': date1.strftime('%Y-%m-%d')},
             'summary': 'Event 2'},
            {'id': 3, 'start': {'date': date2.strftime('%Y-%m-%d')},
             'summary': 'Event 3'},
            {'id': 4, 'start': {'date': date3.strftime('%Y-%m-%dT%H:%M:%S')},
             'summary': 'Event 4'}
        ]
        event = self.calendar.get_current_event(items)

        self.assertEqual(None, self.calendar.get_current_event([]))
        self.assertEqual(now.strftime('%H:%M'), event['start'])
        self.assertEqual('Event 1', event['summary'])

    def test_get_current_event_closest_today(self):
        now = datetime.now()
        date1 = now - timedelta(days=10)
        date2 = now - timedelta(days=7)
        date3 = now - timedelta(days=5)
        date4 = now - timedelta(days=1)
        items = [
            {'id': 1, 'start': {'date': date1.strftime('%Y-%m-%d')},
             'summary': 'Event 1'},
            {'id': 2,
             'start': {'dateTime': date2.strftime('%Y-%m-%dT%H:%M:%S')},
             'summary': 'Event 2'},
            {'id': 3, 'start': {'date': date3.strftime('%Y-%m-%d')},
             'summary': 'Event 3'},
            {'id': 4, 'start': {'date': date4.strftime('%Y-%m-%dT%H:%M:%S')},
             'summary': 'Event 4'}
        ]
        event = self.calendar.get_current_event(items)

        self.assertEqual(date1.strftime('%H:%M'), event['start'])
        self.assertEqual('Event 4', event['summary'])

    def test_get_events(self):
        now = datetime.now()
        date1 = now + timedelta(days=1)
        date2 = now + timedelta(days=5)
        date3 = now + timedelta(days=7)
        items = [
            {'id': 1, 'start': {'dateTime': now.strftime('%Y-%m-%dT%H:%M:%S')},
             'summary': 'Event 1'},
            {'id': 2, 'start': {'date': date1.strftime('%Y-%m-%d')},
             'summary': 'Event 2'},
            {'id': 3, 'start': {'date': date2.strftime('%Y-%m-%d')},
             'summary': 'Event 3'},
            {'id': 4, 'start': {'date': date3.strftime('%Y-%m-%dT%H:%M:%S')},
             'summary': 'Event 4'}
        ]
        self.assertEqual(None, self.calendar.get_events([], None))
        self.assertEqual(3, len(self.calendar.get_events(items, items[0])))
        self.assertEqual(4, len(self.calendar.get_events(items, None)))


class Gmail(unittest.TestCase):

    def setUp(self):
        self.gmail = gmail.Gmail({'interval': None, 'email': None,
                                 'password': None, 'folder': None})

    def test_parse_count(self):
        self.assertEqual(0, self.gmail._parse_count('foo bar'))
        self.assertEqual(10, self.gmail._parse_count('"INBOX" (UNSEEN 10)'))
        self.assertEqual(20, self.gmail._parse_count('"INBOX" (MESSAGES 20)'))


if __name__ == '__main__':
    unittest.main()
