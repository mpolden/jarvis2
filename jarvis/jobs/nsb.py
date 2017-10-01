#!/usr/bin/env python

import requests
from datetime import datetime
from jobs import AbstractJob
from bs4 import BeautifulSoup


class Nsb(AbstractJob):

    def __init__(self, conf):
        self.from_location = conf['from']
        self.to_location = conf['to']
        self.interval = conf['interval']
        self.timeout = conf.get('timeout')

    def _parse(self, html):
        d = BeautifulSoup(html, 'html.parser')

        def is_time(el):
            classes = el.attrs.get('class', [])
            return not any(cls in classes for cls in
                           ('nsb-time-corrected', 'nsb-visually-hidden'))

        date = d.select_one('.travel-date').text.strip()
        all_times = [el.text.strip() for el in d.select('.nsb-time span')
                     if is_time(el)]
        durations = [el.text.strip() for el in d.select('.nsb-time-total')]

        departure_times = all_times[::2]  # filter even elements
        arrival_times = all_times[1::2]  # filter odd elements

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
            'date': now.strftime('%d.%m.%Y'),
            'hour': 'now',
            'redirect_to': 'https://www.nsb.no/bestill/velg-togavgang',
            'travelPlannerStationValidatorVersion': 'v1'
        }

        url = 'https://www.nsb.no/bestill/travel-planner-validator-v2'
        r = requests.get(url, timeout=self.timeout, params=params)
        r.raise_for_status()
        return self._parse(r.text)
