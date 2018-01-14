# -*- coding: utf-8 -*-

import requests
from datetime import datetime, timedelta
from jobs import AbstractJob
from xml.etree import ElementTree as etree


class Yr(AbstractJob):

    def __init__(self, conf):
        self.url = conf['url']
        self.interval = conf['interval']
        self.timeout = conf.get('timeout')
        self.forecast_fallback = conf.get('forecast_fallback', True)

    def _find_tag(self, root, tag):
        return next(iter(root.findall(tag)), None)

    def _parse_wind(self, windSpeed, windDirection):
        if None in (windSpeed, windDirection):
            return None
        return {
            'speed': windSpeed.get('mps'),
            'description': windSpeed.get('name'),
            'direction': windDirection.get('name')
        }

    def _parse_tree(self, tree, date=None):
        if date is None:
            tabular = tree.findall('./forecast/tabular/time[1]').pop()
            root = tree.findall('./observations/weatherstation[1]').pop()
        else:
            date_prefix = date.strftime('%F')
            period_xpath = "./forecast/tabular/time[@period='2']"
            tabular = next((el for el in tree.findall(period_xpath)
                            if el.get('from').startswith(date_prefix)))
            root = tabular

        temperature = self._find_tag(root, 'temperature')
        # Fall back to forecast if weather station is not reporting any data
        if temperature is None and self.forecast_fallback:
            root = tabular
            temperature = self._find_tag(root, 'temperature')
        windSpeed = self._find_tag(root, 'windSpeed')
        windDirection = self._find_tag(root, 'windDirection')

        wind = self._parse_wind(windSpeed, windDirection)
        if temperature is not None:
            temperature = temperature.get('value')
        return {
            'location': tree.findall('./location/name').pop().text,
            'description': tabular.findall('symbol').pop().get('name'),
            'temperature': temperature,
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
