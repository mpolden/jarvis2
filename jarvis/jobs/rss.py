# -*- coding: utf-8 -*-

import requests

from jobs import AbstractJob
from xml.etree import ElementTree as etree
from email.utils import parsedate_tz, mktime_tz


class Rss(AbstractJob):

    def __init__(self, conf):
        self.url = conf['url']
        self.title = conf.get('title')
        self.interval = conf['interval']
        self.timeout = conf.get('timeout')

    def _parse(self, xml):
        tree = etree.fromstring(xml.encode('utf-8'))
        items = []
        for item in tree.findall('./channel/item'):
            title = item.find('title').text
            pubDate = item.find('pubDate').text
            time = mktime_tz(parsedate_tz(pubDate))
            items.append({
                'title': title,
                'time': time
            })
        title = self.title
        if title is None:
            title = tree.find('./channel/title').text
        return {'title': title, 'items': items}

    def get(self):
        r = requests.get(self.url, timeout=self.timeout)
        r.raise_for_status()
        return self._parse(r.text)
