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

    def _find(self, element, path):
        return next(iter(element.findall(path)), None)

    def _parse_location(self, element):
        location = self._find(element, './location/name')
        if location is None:
            return None
        return location.text

    def _parse_temperature(self, element):
        temperature = self._find(element, 'temperature')
        if temperature is None:
            return None
        return temperature.get('value')

    def _parse_description(self, element):
        description = self._find(element, 'symbol')
        if description is None:
            return None
        return description.get('name')

    def _parse_wind(self, element):
        speed = self._find(element, 'windSpeed')
        direction = self._find(element, 'windDirection')
        if None in (speed, direction):
            return None
        return {
            'speed': speed.get('mps'),
            'description': speed.get('name'),
            'direction': direction.get('name')
        }

    def _parse_value(self, observations, parse_fn):
        if len(observations) == 0:
            raise ValueError('No observations found')
        for observation in observations:
            value = parse_fn(observation)
            if value is None and self.forecast_fallback:
                continue
            return value

    def _find_observations(self, tree, date=None):
        observations = []
        if date is None:
            station = self._find(tree, './observations/weatherstation[1]')
            if station is not None:
                observations.append(station)
            tabular = self._find(tree, './forecast/tabular/time[1]')
            if tabular is not None:
                observations.append(tabular)
        else:
            date_prefix = date.strftime('%F')
            period_xpath = "./forecast/tabular/time[@period='2']"
            tabular = next((el for el in tree.findall(period_xpath)
                            if el.get('from').startswith(date_prefix)))
            if tabular is not None:
                observations.append(tabular)
        return observations

    def _parse_tree(self, tree, date=None):
        location = self._parse_location(tree)
        observations = self._find_observations(tree, date)
        temperature = self._parse_value(observations, self._parse_temperature)
        description = self._parse_value(observations, self._parse_description)
        wind = self._parse_value(observations, self._parse_wind)
        return {
            'location': location,
            'description': description,
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
