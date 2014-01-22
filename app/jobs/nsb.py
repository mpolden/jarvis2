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

        date = d.find('.date')[0].text_content().strip()
        departure_times = [el.text_content().strip() for el in
                           d.find('.depart')]
        arrival_times = [el.text_content().strip() for el in
                         d.find('.arrive')]
        durations = [int(el.text_content().rstrip(' min')) for el in
                     d.find('.duration')]

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
            'from': self.from_location,
            'to': self.to_location,
            'type': 'single',
            'date': now.strftime('%d.%m.%Y'),
            'hour': now.strftime('%H'),
            'redirect_to': 'https://www.nsb.no/bestill/velg-togavgang'
        }
        r = requests.get('https://www.nsb.no/bestill/travel-planner-validator',
                         params=params)

        if r.status_code == 200 and len(r.content) > 0:
            return self._parse(r.content)
        return {}
