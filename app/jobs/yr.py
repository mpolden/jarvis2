#!/usr/bin/env python

import requests
from datetime import datetime, timedelta
from jobs import AbstractJob
from lxml import etree


class Yr(AbstractJob):

    def __init__(self, conf):
        self.url = conf['url']
        self.interval = conf['interval']

    def _parse_tree(self, tree, tabular_xpath=None):
        if tabular_xpath is None:
            tabular = tree.xpath('/weatherdata/forecast/tabular/time[1]').pop()
            data_root = tree.xpath(
                '/weatherdata/observations/weatherstation[1]').pop()
        else:
            tabular = tree.xpath(tabular_xpath).pop()
            data_root = tabular

        windSpeed = data_root.xpath('windSpeed').pop()
        return {
            'location': tree.xpath('/weatherdata/location/name').pop().text,
            'temperature': data_root.xpath('temperature').pop().get('value'),
            'description': tabular.xpath('symbol').pop().get('name'),
            'wind': {
                'speed': windSpeed.get('mps'),
                'description': windSpeed.get('name'),
                'direction': data_root.xpath('windDirection').pop().get('name')
            }
        }

    def _parse_tree_date(self, tree, date=None):
        if date is None:
            date = datetime.now().date() + timedelta(days=1)
        xpath = ('/weatherdata/forecast/tabular/time[@period=2 and'
                 ' starts-with(@from, "%s")]') % (date.strftime('%F'),)
        return self._parse_tree(tree, xpath)

    def _parse(self, xml):
        tree = etree.fromstring(xml)
        data = self._parse_tree(tree)
        data.update({'tomorrow': self._parse_tree_date(tree)})
        return data

    def get(self):
        r = requests.get(self.url)

        if r.status_code == 200 and len(r.content) > 0:
            return self._parse(r.content)
        return {}
