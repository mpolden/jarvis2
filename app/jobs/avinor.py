#!/usr/bin/env python

import requests
from lxml import etree

from jobs import AbstractJob


class Avinor(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']
        self.from_airport = conf['from']
        self.to_airport = conf['to']
        self.timeout = conf.get('timeout')

    def _parse(self, xml):
        tree = etree.fromstring(xml)

        flights = []
        for flight in tree.xpath('/airport/flights/flight'):
            airport = flight.xpath('airport').pop().text
            if self.to_airport is not None and airport != self.to_airport:
                continue

            flights.append({
                'airport': airport,
                'schedule_time': flight.xpath('schedule_time').pop().text,
                'flight_id': flight.xpath('flight_id').pop().text
            })

        return {
            'from': self.from_airport,
            'to': self.to_airport,
            'flights': flights
        }

    def get(self):
        params = {
            'timeFrom': 0,
            'timeTo': 24,
            'airport': self.from_airport,
            'direction': 'D'
        }
        r = requests.get('http://flydata.avinor.no/XmlFeed.asp',
                         timeout=self.timeout, params=params)
        r.raise_for_status()
        return self._parse(r.content)
