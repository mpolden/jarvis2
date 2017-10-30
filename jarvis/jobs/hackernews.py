# -*- coding: utf-8 -*-

import requests
from jobs import AbstractJob
from bs4 import BeautifulSoup


class HackerNews(AbstractJob):

    def __init__(self, conf):
        self.url = 'https://news.ycombinator.com'
        self.interval = conf['interval']
        self.timeout = conf.get('timeout')

    def _parse(self, html):
        d = BeautifulSoup(html, 'html.parser')

        def source_link(el): return el.attrs.get('href', '').startswith('from')

        def more_link(el): return el.text == 'More'

        titles = [el.text for el in d.select('td.title a')
                  if not source_link(el) and not more_link(el)]

        points = [int(el.text.rstrip(' points')) for el in
                  d.select('td.subtext span.score')]

        items = []
        for title, num_points in zip(titles, points):
            items.append({
                'title': title,
                'points': num_points
            })

        return {'items': items}

    def get(self):
        r = requests.get(self.url, timeout=self.timeout)
        r.raise_for_status()
        return self._parse(r.text)
