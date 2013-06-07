#!/usr/bin/env python

import requests
import json
from lxml import etree


class Yr(object):

    def __init__(self, conf):
        self.url = conf['yr']['url']
        self.every = conf['yr']['every']

    def get(self):
        # Retrieve XML data from YR_URL
        r = requests.get(self.url)

        # Parse XML string into an ElementTree
        tree = etree.fromstring(r.content)

        # Use XPath to get the values we're interested in
        tabular = tree.xpath('/weatherdata/forecast/tabular/time[1]').pop()
        weatherStation = tree.xpath(
            '/weatherdata/observations/weatherstation[1]').pop()
        windSpeed = weatherStation.xpath('windSpeed').pop()
        data = {
            'location': tree.xpath('/weatherdata/location/name').pop().text,
            'temperature': weatherStation.xpath('temperature').pop().get(
                'value'),
            'description': tabular.xpath('symbol').pop().get('name'),
            'wind': {
                'speed': windSpeed.get('mps'),
                'description': windSpeed.get('name'),
                'direction': weatherStation.xpath('windDirection').pop().get(
                    'name')
            }
        }
        return json.dumps(data)


if __name__ == '__main__':
    yr = Yr({
            'yr': {
                'url': ('http://www.yr.no/sted/Norge/S%C3%B8r-Tr%C3%B8ndelag/'
                        'Trondheim/Trondheim/varsel.xml'),
                'every': 10
            }
            })
    print yr.get()
