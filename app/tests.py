#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import unittest
from datetime import datetime
from jobs import yr, hackernews, nsb, ping, calendar
from lxml import etree


class Yr(unittest.TestCase):

    def setUp(self):
        xml_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                'test_data', 'varsel.xml'))
        with open(xml_path, 'rb') as f:
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
        data = y._parse_tree(self.tree, datetime(2013, 7, 1))

        self.assertEqual('Regn', data['description'])
        self.assertEqual('Trondheim', data['location'])
        self.assertEqual('23', data['temperature'])
        self.assertEqual(u'Sør', data['wind']['direction'])
        self.assertEqual('3.6', data['wind']['speed'])
        self.assertEqual('Lett bris', data['wind']['description'])

    def test_parse_tree_missing_wind(self):
        xml_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                'test_data', 'varsel2.xml'))
        with open(xml_path, 'rb') as f:
            tree = etree.fromstring(f.read())
        y = yr.Yr({'interval': None, 'url': None})
        data = y._parse_tree(tree)
        self.assertTrue(data['wind'] is None)


class HackerNews(unittest.TestCase):

    def setUp(self):
        html_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 'test_data', 'hn.html'))
        with open(html_path, 'r') as f:
            self.html = f.read()
        self.hn = hackernews.HackerNews({'interval': None})

    def test_parse(self):
        data = self.hn._parse(self.html)

        self.assertEqual(28, len(data['items']))
        self.assertTrue('points' in data['items'][3])
        self.assertTrue('title' in data['items'][3])
        self.assertEqual(76, data['items'][3]['points'])
        self.assertEqual('Building an OpenBSD Router',
                         data['items'][3]['title'])


class Nsb(unittest.TestCase):

    def setUp(self):
        test_data = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 'test_data'))
        with open(os.path.join(test_data, 'nsb.html')) as f:
            self.html = f.read()

        self.nsb = nsb.Nsb({'interval': None,
                            'from': 'Skansen',
                            'to': 'V\xc3\xa6rnes (Trondheim Lufthavn)'})

    def test_parse(self):
        # Test data contains multiple dates and varying durations
        data = self.nsb._parse(self.html)

        self.assertEqual('02.10.2016', data['date'])
        self.assertEqual('V\xc3\xa6rnes (Trondheim Lufthavn)', data['to'])
        self.assertEqual('Skansen', data['from'])
        self.assertEqual(5, len(data['departures']))
        self.assertEqual('20:56', data['departures'][0]['departure'])
        self.assertEqual('21:36', data['departures'][0]['arrival'])
        self.assertEqual('40min', data['departures'][0]['duration'])


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
        self.calendar = calendar.Calendar({'interval': None})

    def test_parse(self):
        items = [
            {'id': 'foo1', 'summary': 'Foo bar 1',
             'start': {'dateTime': '2013-07-01T15:00:00+02:00'}},
            {'id': 'foo2', 'summary': 'Foo bar 2',
             'start': {'dateTime': '2013-08-01T15:00:00+02:00'}},
        ]
        expected = [{'date': '2013-07-01T15:00:00+02:00', 'id': 'foo1',
                     'summary': 'Foo bar 1'},
                    {'date': '2013-08-01T15:00:00+02:00', 'id': 'foo2',
                     'summary': 'Foo bar 2'}]
        self.assertEqual(self.calendar._parse(items), expected)


if __name__ == '__main__':
    unittest.main()
