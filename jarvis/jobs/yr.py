#!/usr/bin/env python

import requests
from datetime import datetime, timedelta
from jobs import AbstractJob
from xml.etree import ElementTree as etree


class Yr(AbstractJob):

    def __init__(self, conf):
        self.url = conf['url']
        self.interval = conf['interval']
        self.timeout = conf.get('timeout')

    def _parse_tree(self, tree, date=None):
        if date is None:
            tabular = tree.findall('./forecast/tabular/time[1]').pop()
            data_root = tree.findall('./observations/weatherstation[1]').pop()
        else:
            date_prefix = date.strftime('%F')
            period_xpath = "./forecast/tabular/time[@period='2']"
            tabular = next((el for el in tree.findall(period_xpath)
                            if el.get('from').startswith(date_prefix)))
            data_root = tabular

        windSpeed = next(iter(data_root.findall('windSpeed')), None)
        windDirection = next(iter(data_root.findall('windDirection')), None)

        wind = None
        if None not in (windSpeed, windDirection):
            wind = {
                'speed': windSpeed.get('mps'),
                'description': windSpeed.get('name'),
                'direction': windDirection.get('name')
            }

        return {
            'location': tree.findall('./location/name').pop().text,
            'temperature': data_root.findall('temperature').pop().get('value'),
            'description': tabular.findall('symbol').pop().get('name'),
            'wind': wind
        }

    def _parse(self, xml):
        tree = etree.fromstring(xml)
        tomorrow = datetime.now().date() + timedelta(days=1)
        return {
            'today': self._parse_tree(tree),
            'tomorrow': self._parse_tree(tree, tomorrow)
        }

    def get(self):
        r = requests.get(self.url, timeout=self.timeout)
        r.raise_for_status()
        return self._parse(r.content)
