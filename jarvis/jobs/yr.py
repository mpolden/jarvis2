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

    def _parse_location(self, element):
        location = element.find('./location/name')
        if location is None:
            return None
        return location.text

    def _parse_temperature(self, element):
        temperature = element.find('temperature')
        if temperature is None:
            return None
        return temperature.get('value')

    def _parse_description(self, element):
        description = element.find('symbol')
        if description is None:
            return None
        return description.get('name')

    def _parse_wind(self, element):
        speed = element.find('windSpeed')
        direction = element.find('windDirection')
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

    def _find_observations(self, element, date=None):
        if date is not None:
            date_prefix = date.strftime('%F')
            # period='2' identifies afternoon
            period_xpath = "./forecast/tabular/time[@period='2']"
            return [el for el in element.findall(period_xpath)
                    if el.get('from').startswith(date_prefix)]
        elements = (
            element.find('./observations/weatherstation[1]'),
            element.find('./forecast/tabular/time[1]'),
        )
        return [el for el in elements if el is not None]

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
        return self._parse(r.text)
