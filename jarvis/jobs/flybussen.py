# -*- coding: utf-8 -*-

import json
import requests

from datetime import datetime, timedelta
from jobs import AbstractJob


class Flybussen(AbstractJob):

    def __init__(self, conf):
        self.to_airport = conf['to_airport'].upper()
        self.from_stop = conf['from_stop']
        self.interval = conf['interval']
        self.timeout = conf.get('timeout')
        self.base_url = conf.get('base_url', 'https://www.flybussen.no')
        self.now = datetime.now

    def _stop(self):
        url = '{}/server/wsapi/stop/format/json/p/web/v/1'.format(
            self.base_url
        )
        params = (
            ('action', 'departures'),
            ('airport_code', self.to_airport),
            ('product_id', 1)
        )
        r = requests.get(url, params=params, timeout=self.timeout)
        r.raise_for_status()
        stops = r.json()
        return next((stop for stop in stops['data']
                    if stop['stop_name'].lower() == self.from_stop.lower()),
                    None)

    def _airport(self):
        url = '{}/server/wsapi/airport/format/json/p/web/v/1'.format(
            self.base_url
        )
        r = requests.get(url, timeout=self.timeout)
        r.raise_for_status()
        airports = r.json()
        return next((airport for airport in airports['data']
                    if airport['code'] == self.to_airport),
                    None)

    def _trip(self, stop, airport, dt):
        url = '{}/server/api/travel/format/json/p/web/v/1'.format(
            self.base_url
        )
        data = {
            'from_stop_id': stop['stop_id'],
            'to_stop_id': airport['stops'][0]['id'],
            'from_date': dt.strftime('%Y-%m-%d'),
            'to_date': None,
            'from_time': dt.strftime('%H:%M'),
            'airport_code': self.to_airport
        }
        params = {'data': json.dumps(data, sort_keys=True)}
        r = requests.get(url, params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def _departures(self, trip):
        return [{'stop_name': self.from_stop,
                 'departure_time': departure['start_departure_ts']}
                for departure in trip['trip']['trip_container']]

    def get(self):
        airport = self._airport()
        if airport is None:
            raise ValueError('No airport with code: {}'.format(
                self.to_airport))
        if len(airport['stops']) == 0:
            raise ValueError('No stops found for airport: {}'.format(
                self.to_airport))

        stop = self._stop()
        if stop is None:
            raise ValueError('No stop ID found with name: {}'.format(
                self.from_stop))

        from_ = stop['stop_name']
        to = airport['stops'][0]['name']
        dt = self.now()
        trip = self._trip(stop, airport, dt)
        if len(trip['trip']['trip_container']) == 0:
            # No more departures today, try next day
            dt = (dt + timedelta(days=1)).date()
            trip = self._trip(stop, airport, dt)
        departures = self._departures(trip)
        return {
            'from': from_,
            'to': to,
            'departures': departures
        }
