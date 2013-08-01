#!/usr/bin/env python

import dateutil.parser
import requests
from jobs import AbstractJob
from lxml import etree


class Avinor(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']
        self.from_airport = conf['from']
        self.to_airport = conf['to']

    def _parse(self, xml):
        tree = etree.fromstring(xml)

        flights = []
        for flight in tree.xpath('/airport/flights/flight'):
            airport = flight.xpath('airport').pop().text
            if self.to_airport is not None and airport != self.to_airport:
                continue

            schedule_time = dateutil.parser.parse(flight.xpath(
                'schedule_time').pop().text).strftime('%Y-%m-%dT%H:%M:%S')
            flights.append({
                'airport': airport,
                'schedule_time': schedule_time,
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
        r = requests.get('http://flydata.avinor.no/XmlFeed.asp', params=params)

        if r.status_code == 200 and len(r.content) > 0:
            return self._parse(r.content)
        return {}
