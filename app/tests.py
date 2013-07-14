#!/usr/bin/env python

import jobs
import json
import os.path
import unittest
from datetime import datetime


class Yr(unittest.TestCase):

    def setUp(self):
        xml_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   'test_data',
                                   'varsel.xml'))
        with open(xml_path, 'r') as f:
            self.xml = f.read()

    def test_parse(self):
        yr = jobs.Yr({'interval': None, 'url': None})
        data = yr._parse(self.xml)

        self.assertEqual('Delvis skyet', data['description'])
        self.assertEqual('Trondheim', data['location'])
        self.assertEqual('16.3', data['temperature'])
        self.assertEqual('Nord', data['wind']['direction'])
        self.assertEqual('0.7', data['wind']['speed'])
        self.assertEqual('Flau vind', data['wind']['description'])


class Atb(unittest.TestCase):

    def setUp(self):
        json_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                    'test_data',
                                    'atb.json'))
        with open(json_path, 'r') as f:
            self.json = json.loads(f.read())

    def test_parse(self):
        atb = jobs.Atb({'interval': None, 'url': None})
        now = datetime.now()
        data = atb._parse(self.json, now=datetime(now.year, now.month, now.day,
                                                  21, 30, 0, 0))

        departures = data['departures']
        self.assertEqual(5, len(departures))
        self.assertEqual(5, departures[0]['eta'])
        self.assertEqual(5, departures[1]['eta'])
        self.assertEqual(5, departures[2]['eta'])
        self.assertEqual(8, departures[3]['eta'])
        self.assertEqual(10, departures[4]['eta'])

    def test_parse_gt_or_eq_zero(self):
        atb = jobs.Atb({'interval': None, 'url': None})
        now = datetime.now()
        data = atb._parse(self.json, now=datetime(now.year, now.month, now.day,
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
        self.hn = jobs.HackerNews({'interval': None})

    def test_parse(self):
        data = self.hn._parse(self.html)

        self.assertEqual(29, len(data['items']))
        self.assertTrue('points' in data['items'][0])
        self.assertTrue('title' in data['items'][0])
        self.assertEqual(220, data['items'][0]['points'])
        self.assertEqual('Do Things that Don\'t Scale',
                         data['items'][0]['title'])


if __name__ == '__main__':
    unittest.main()
