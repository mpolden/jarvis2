#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import os.path
import unittest

from app import app
from datetime import datetime
from jobs import (avinor, calendar, flybussen, hackernews, nsb, ping, rss,
                  vaernesekspressen, yr)
from multiprocessing import Process, set_start_method
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from tempfile import mkdtemp
from xml.etree import ElementTree as etree
from util.create_dashboard import DashboardFactory
from util.create_widget import WidgetFactory
from werkzeug.serving import run_simple
from http.server import BaseHTTPRequestHandler, HTTPServer


class TestRequestHandler(BaseHTTPRequestHandler):

    def _response(self):
        return self.server.test_responses.get(self.command, {}).get(self.path)

    def _write_response(self):
        response = self._response()
        status_code = 200
        if response is None:
            status_code = 404
            response = {'error': 'No match for {} {}'.format(self.command,
                                                             self.path)}
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_GET(self):
        self._write_response()

    def do_POST(self):
        self._write_response()

    def log_message(self, format, *args):
        # Disable request logging
        return


def test_data(name, parse_json=False):
    path = os.path.join(os.path.dirname(__file__), 'test_data', name)
    with open(path, 'rb') as f:
        if parse_json:
            return json.loads(f.read().decode('utf-8'))
        else:
            return f.read()


class App(unittest.TestCase):

    def setUp(self):
        app.testing = True
        app.debug = True
        app.config['DEFAULT_LAYOUT'] = None
        app.config['JOBS'] = {
            'mock': {
                'enabled': True,
                'interval': 60
            }
        }
        app.logger.setLevel(logging.WARN)
        logging.getLogger('werkzeug').setLevel(logging.WARN)
        # Run the application in a separate process so that streamed responses
        # are not blocked on running the client in the same thread
        self.p = Process(target=run_simple, args=('127.0.0.1', 8080, app),
                         kwargs={'use_debugger': app.debug})
        self.p.start()

    def url(self, path):
        return 'http://127.0.0.1:8080' + path

    def session(self):
        s = Session()
        s.mount('http://', HTTPAdapter(
            max_retries=Retry(total=100, backoff_factor=0.1))
        )
        return s

    def get(self, path, **kwargs):
        return self.session().get(self.url(path), **kwargs)

    def post(self, path, **kwargs):
        return self.session().post(self.url(path), **kwargs)

    def test_widget(self):
        r = self.get('/widget/foo')
        self.assertEqual(404, r.status_code)

        r = self.get('/widget/mock')
        self.assertEqual(200, r.status_code)
        self.assertEqual('text/html; charset=utf-8', r.headers['content-type'])

        r = self.get('/w/mock')
        self.assertEqual(200, r.status_code)
        self.assertEqual('text/html; charset=utf-8', r.headers['content-type'])

    def test_dashboard(self):
        r = self.get('/dashboard/foo')
        self.assertEqual(404, r.status_code)

        r = self.get('/')
        self.assertEqual(200, r.status_code)
        self.assertEqual('text/html; charset=utf-8', r.headers['content-type'])

    def test_events(self):
        r = self.get('/events', stream=True)
        with r:
            data = next(r.iter_lines(chunk_size=1)).decode('utf-8')
        self.assertEqual(200, r.status_code)
        self.assertEqual('text/event-stream; charset=utf-8',
                         r.headers['content-type'])
        self.assertEqual('data: {"body":{"data":"spam"},"job":"mock"}', data)

    def test_events_post(self):
        r = self.post('/events/foo')
        self.assertEqual(404, r.status_code)

        r = self.post('/events/mock', json={'data': 'eggs'})
        self.assertEqual(201, r.status_code)

        r = self.get('/events', stream=True)
        with r:
            data = next(r.iter_lines(chunk_size=1)).decode('utf-8')
        self.assertEqual(200, r.status_code)
        self.assertEqual('text/event-stream; charset=utf-8',
                         r.headers['content-type'])
        self.assertEqual('data: {"body":{"data":"eggs"},"job":"mock"}', data)

    def tearDown(self):
        self.p.terminate()
        self.p.join()


class Yr(unittest.TestCase):

    def setUp(self):
        self.tree = etree.fromstring(test_data('varsel.xml'))

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

    def test_parse_tree_missing_wind_from_weather_station(self):
        tree = etree.fromstring(test_data('varsel2.xml'))
        y = yr.Yr({'interval': None, 'url': None})
        data = y._parse_tree(tree)
        self.assertEqual(u'Vest-sørvest', data['wind']['direction'])
        self.assertEqual('10.0', data['wind']['speed'])
        self.assertEqual('Frisk bris', data['wind']['description'])

    def test_parse_tree_missing_temperature(self):
        tree = etree.fromstring(test_data('varsel3.xml'))
        y = yr.Yr({'interval': None, 'url': None, 'forecast_fallback': False})
        data = y._parse_tree(tree)
        self.assertIsNone(data['temperature'])

    def test_parse_tree_forecast_fallback(self):
        tree = etree.fromstring(test_data('varsel4.xml'))
        y = yr.Yr({'interval': None, 'url': None})
        data = y._parse_tree(tree)

        self.assertEqual('Lettskyet', data['description'])
        self.assertEqual('Trondheim', data['location'])
        self.assertEqual('-3', data['temperature'])
        self.assertEqual(u'Sør', data['wind']['direction'])
        self.assertEqual('8.6', data['wind']['speed'])
        self.assertEqual('Frisk bris', data['wind']['description'])

    def test_parse_tree_weather_station_removed(self):
        tree = etree.fromstring(test_data('varsel5.xml'))
        y = yr.Yr({'interval': None, 'url': None})
        data = y._parse_tree(tree)

        self.assertEqual('Skyet', data['description'])
        self.assertEqual('Trondheim', data['location'])
        self.assertEqual('-1', data['temperature'])
        self.assertEqual(u'Sør-sørvest', data['wind']['direction'])
        self.assertEqual('0.6', data['wind']['speed'])
        self.assertEqual('Flau vind', data['wind']['description'])


class HackerNews(unittest.TestCase):

    def setUp(self):
        self.html = test_data('hn.html')
        self.hn = hackernews.HackerNews({'interval': None})

    def test_parse(self):
        data = self.hn._parse(self.html)

        self.assertEqual(30, len(data['items']))
        self.assertTrue('points' in data['items'][3])
        self.assertTrue('title' in data['items'][3])
        self.assertEqual(76, data['items'][3]['points'])
        self.assertEqual('Building an OpenBSD Router',
                         data['items'][3]['title'])


class Nsb(unittest.TestCase):

    def setUp(self):
        self.json = test_data('nsb.json', parse_json=True)
        self.nsb = nsb.Nsb({'interval': None,
                            'from': 'Skansen',
                            'to': 'V\xc3\xa6rnes (Trondheim Lufthavn)'})

    def test_parse(self):
        data = self.nsb._parse(self.json)

        self.assertEqual('V\xc3\xa6rnes (Trondheim Lufthavn)', data['to'])
        self.assertEqual('Skansen', data['from'])
        self.assertEqual(5, len(data['departures']))
        self.assertEqual('2018-05-31T17:03:00',
                         data['departures'][0]['departure'])
        self.assertEqual('2018-05-31T17:42:00',
                         data['departures'][0]['arrival'])
        self.assertEqual(2340, data['departures'][0]['duration'])


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


class Avinor(unittest.TestCase):

    def setUp(self):
        self.xml = test_data('flights.xml')

    def test_parse(self):
        a = avinor.Avinor({'interval': None,
                           'url': None,
                           'from': 'TRD',
                           'to': 'OSL'})
        data = a._parse(self.xml)
        self.assertEqual(34, len(data['flights']))


class Flybussen(unittest.TestCase):

    def _test_responses(self):
        airport_path = '/server/wsapi/airport/format/json/p/web/v/1'
        stop_path = ('/server/wsapi/stop/format/json/p/web/v/1'
                     '?action=departures&airport_code=TRD&product_id=1')
        trip_path = ('/server/api/travel/format/json/p/web/v/1?data=%7B%22'
                     'airport_code%22%3A+%22TRD%22%2C+%22'
                     'from_date%22%3A+%222017-10-27%22%2C+%22'
                     'from_stop_id%22%3A+%227146%22%2C+%22'
                     'from_time%22%3A+%2220%3A25%22%2C+%22'
                     'to_date%22%3A+null%2C+%22to_stop_id%22%3A+%22150%22%7D')
        return {
            'GET': {
                airport_path: test_data('flybussen_airport.json', True),
                stop_path: test_data('flybussen_stop.json', True),
                trip_path: test_data('flybussen_trip.json', True),
            }
        }

    @property
    def url(self):
        return 'http://{}:{}'.format(self.listen[0], self.listen[1])

    def setUp(self):
        self.listen = ('127.0.0.1', 8080)
        self.server = HTTPServer(self.listen, TestRequestHandler)
        self.server.test_responses = self._test_responses()
        self.p = Process(target=self.server.serve_forever)
        self.p.start()

    def test_get(self):
        f = flybussen.Flybussen({
            'interval': None,
            'from_stop': 'Dronningens gate D2',
            'to_airport': 'TRD',
            'base_url': self.url
        })
        f.now = lambda: datetime(2017, 10, 27, 20, 25)
        data = f.get()
        self.assertEqual(26, len(data['departures']))
        self.assertEqual('1509116640', data['departures'][0]['departure_time'])
        self.assertEqual('Dronningens gate D2',
                         data['departures'][0]['stop_name'])
        self.assertEqual('Dronningens gate D2', data['from'])
        self.assertEqual(u'Trondheim lufthavn Værnes', data['to'])

    def tearDown(self):
        self.server.socket.close()
        self.p.terminate()
        self.p.join()


class Vaernesekspressen(unittest.TestCase):

    def _test_responses(self):
        stop_path = ('/Umbraco/Api/TicketOrderApi/GetStops?routeId=31')
        departure_path = ('/Umbraco/Api/TicketOrderApi/GetJourneys')
        return {
            'GET': {
                stop_path: test_data('vaernesekspressen_stops.json', True),
            },
            'POST': {
                departure_path: test_data('vaernesekspressen_departures.json',
                                          True)
            }
        }

    @property
    def url(self):
        return 'http://{}:{}'.format(self.listen[0], self.listen[1])

    def setUp(self):
        self.listen = ('127.0.0.1', 8080)
        self.server = HTTPServer(self.listen, TestRequestHandler)
        self.server.test_responses = self._test_responses()
        self.p = Process(target=self.server.serve_forever)
        self.p.start()

    def test_get(self):
        f = vaernesekspressen.Vaernesekspressen({
            'interval': None,
            'from_stop': 'fb 73 nidarosdomen',
            'base_url': self.url
        })
        f.now = lambda: datetime(2020, 2, 1, 10)
        data = f.get()
        self.assertEqual(9, len(data['departures']))
        self.assertEqual('1580570100', data['departures'][0]['departure_time'])
        self.assertEqual('FB 73 Nidarosdomen',
                         data['departures'][0]['stop_name'])
        self.assertEqual('FB 73 Nidarosdomen', data['from'])
        self.assertEqual(u'Trondheim Lufthavn Værnes', data['to'])

    def tearDown(self):
        self.server.socket.close()
        self.p.terminate()
        self.p.join()


class Rss(unittest.TestCase):

    def setUp(self):
        self.xml = test_data('nrk.rss').decode('utf-8')

    def test_parse(self):
        r = rss.Rss({'url': None, 'interval': None})
        data = r._parse(self.xml)
        self.assertEqual('NRK', data['title'])
        self.assertEqual(100, len(data['items']))
        self.assertEqual('Heilt likt i nedrykksstriden',
                         data['items'][0]['title'])
        self.assertEqual(1511117699, data['items'][0]['time'])

        # Override title
        r.title = 'foo'
        data = r._parse(self.xml)
        self.assertEqual('foo', data['title'])


class CreateDashboard(unittest.TestCase):

    def setUp(self):
        self.tmpdir = mkdtemp(prefix='jarvis')
        os.makedirs(os.path.join(self.tmpdir, 'templates', 'layouts'))
        self.factory = DashboardFactory('foo', app_root=self.tmpdir,
                                        quiet=True)

    def test_create_and_remove(self):
        self.factory.create_dashboard()
        self.assertTrue(os.path.exists(self.factory.layout))
        self.factory.remove_dashboard()
        self.assertFalse(os.path.exists(self.factory.layout))

    def tearDown(self):
        os.removedirs(self.factory.layout_dir)


class CreateWidget(unittest.TestCase):

    def setUp(self):
        self.tmpdir = mkdtemp(prefix='jarvis')
        os.makedirs(os.path.join(self.tmpdir, 'jobs'))
        os.makedirs(os.path.join(self.tmpdir, 'static', 'widgets'))
        self.factory = WidgetFactory('foo', app_root=self.tmpdir, quiet=True)

    def test_create_and_remove(self):
        self.factory.create_widget()
        assets = ['foo.js', 'foo.css']
        for asset in assets:
            self.assertTrue(os.path.exists(os.path.join(
                self.factory.widget_dir, asset)))
        self.assertTrue(os.path.exists(self.factory.job_file))

        self.factory.remove_widget()
        for asset in assets:
            self.assertFalse(os.path.exists(os.path.join(
                self.factory.widget_dir, asset)))
        self.assertFalse(os.path.exists(self.factory.job_file))

    def tearDown(self):
        os.removedirs(os.path.dirname(self.factory.job_file))
        os.removedirs(os.path.dirname(self.factory.widget_dir))


if __name__ == '__main__':
    # 3.8 changed default method 'spawn' on macOS, however werkzeug doesn't
    # work with spawn.
    # https://bugs.python.org/issue33725
    set_start_method('fork')
    unittest.main()
