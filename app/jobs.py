#!/usr/bin/env python

import requests
import json
from datetime import datetime
from lxml import etree
from soco import SoCo


class Base(object):

    def get(self):
        raise NotImplementedError('Needs to be implemented')


class Yr(Base):

    def __init__(self, conf):
        self.url = conf['url']
        self.interval = conf['interval']

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
        return data


class Atb(Base):

    def __init__(self, conf):
        self.url = conf['url']
        self.interval = conf['interval']

    def get(self):
        r = requests.get(self.url)

        if r.status_code == 200 and len(r.content) > 0:
            data = json.loads(r.content)
            for departure in data['departures']:
                departureTime = datetime.strptime(
                    departure['registeredDepartureTime'],
                    '%Y-%m-%dT%H:%M:%S.000')
                remaining = (departureTime - datetime.now()
                             ).total_seconds() / 60
                departure['hour'] = departureTime.strftime('%H')
                departure['minute'] = departureTime.strftime('%M')
                if remaining > 0:
                    departure['remaining'] = int(remaining)
                else:
                    departure['remaining'] = 0

            return data
        return {}


class HackerNews(Base):

    def __init__(self, conf):
        self.url = conf['url']
        self.interval = conf['interval']

    def get(self):
        r = requests.get(self.url)

        if r.status_code == 200 and len(r.content) > 0:
            return json.loads(r.content)
        return {}


class Sonos(Base):

    def __init__(self, conf):
        self.ip = conf['ip']
        self.interval = conf['interval']

    def get(self):
        sonos = SoCo(self.ip)

        np = sonos.get_current_track_info()
        next = sonos.get_queue(int(np['playlist_position']), 1).pop()
        return {
            'name': sonos.get_speaker_info()['zone_name'],
            'np': np,
            'next': next
        }


if __name__ == '__main__':
    yr = Yr({
            'url': ('http://www.yr.no/sted/Norge/S%C3%B8r-Tr%C3%B8ndelag/'
                    'Trondheim/Trondheim/varsel.xml'),
            'interval': 10
            })
    print yr.get()
