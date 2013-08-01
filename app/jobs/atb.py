#!/usr/bin/env python

import dateutil.parser
import requests
from datetime import datetime
from jobs import AbstractJob


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
