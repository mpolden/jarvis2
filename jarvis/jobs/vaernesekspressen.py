# -*- coding: utf-8 -*-

import requests

from datetime import datetime, timedelta
from jobs import AbstractJob


class Vaernesekspressen(AbstractJob):

    def __init__(self, conf):
        self.airport_id = 113  # Vaernes is the the only supported destionation
        self.from_stop = conf['from_stop']
        self.interval = conf['interval']
        self.timeout = conf.get('timeout')
        self.base_url = conf.get('base_url',
                                 'https://www.vaernesekspressen.no')
        self.now = datetime.now

    def _find_stop_id(self):
        url = '{}/Umbraco/Api/TicketOrderApi/GetStops'.format(self.base_url)
        params = {'routeId': 31}  # There is only one route
        r = requests.get(url, params=params, timeout=self.timeout)
        r.raise_for_status()
        for stop in r.json():
            if stop['Name'].lower() == self.from_stop.lower():
                return stop['Id']
        raise ValueError(
            'Could not find ID for stop "{}"'.format(self.from_stop))

    def _timestamp(self, dt, tz):
        # I hate Python.
        utc_offset = timedelta(0)
        if tz == 'CET':
            utc_offset = timedelta(hours=1)
        elif tz == 'CEST':
            utc_offset = timedelta(hours=2)
        else:
            raise ValueError('Unexpected time zone "{}"'.format(tz))
        epoch = datetime(1970, 1, 1)
        return (dt - utc_offset - epoch).total_seconds()

    def _parse_time(self, date):
        parts = date.rsplit(' ', 1)
        tz = parts[1]
        dt = datetime.strptime(parts[0], '%Y-%m-%d %H:%M:%S.0')
        return int(self._timestamp(dt, tz))

    def _departures(self, stop_id, dt):
        url = '{}/Umbraco/Api/TicketOrderApi/GetJourneys'.format(self.base_url)
        data = {
            'From': str(stop_id),
            'To': str(self.airport_id),
            'Route': '31',
            'Date': dt.strftime('%d.%m.%Y'),
            'Adult': '1',
            'Student': '0',
            'Child': '0',
            'Baby': '0',
            'Senior': '0',
            'isRoundTrip': False,
        }
        r = requests.post(url, json=data, timeout=self.timeout)
        r.raise_for_status()
        return [{'stop_name': d['Start']['Name'],
                 'destination_name': d['End']['Name'],
                 'departure_time': str(self._parse_time(d['DepartureTime']))}
                for d in r.json()]

    def get(self):
        stop_id = self._find_stop_id()
        now = self.now()
        departures = self._departures(stop_id, now)
        if len(departures) < 2:
            # Few departures today, include tomorrow's departures
            tomorrow = (now + timedelta(days=1)).date()
            departures += self._departures(stop_id, tomorrow)
        from_ = 'N/A'
        to = 'N/A'
        if len(departures) > 0:
            from_ = departures[0]['stop_name']
            to = departures[0]['destination_name']
        return {
            'from': from_,
            'to': to,
            'departures': departures
        }
