#!/usr/bin/env python

import requests
from datetime import datetime
from jobs import AbstractJob
from pyquery import PyQuery as pq


class Nsb(AbstractJob):

    def __init__(self, conf):
        self.from_location = conf['from']
        self.to_location = conf['to']
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
        params = {
            'booking-from': self.from_location,
            'booking-to': self.to_location,
            'booking-type': 'single',
            'booking-date': now.strftime('%d-%m-%Y'),
            'booking-date_outward_hour': now.strftime('%H')
        }
        r = requests.get('https://www.nsb.no/category2734.html', params=params)

        if r.status_code == 200 and len(r.content) > 0:
            return self._parse(r.content)
        return {}
