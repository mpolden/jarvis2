#!/usr/bin/env python

import requests
from jobs import AbstractJob
from pyquery import PyQuery as pq


class HackerNews(AbstractJob):

    def __init__(self, conf):
        self.url = 'https://news.ycombinator.com'
        self.interval = conf['interval']

    def _parse(self, html):
        d = pq(html)

        titles = [el.text for el in
                  d.find('td.title a')
                  .not_('a[href="news2"]')
                  .not_('a[href^="item"]')]
        points = [int(el.text.rstrip(' points')) for el in
                  d.find('td.subtext span')]

        items = []
        for title, num_points in zip(titles, points):
            items.append({
                'title': title,
                'points': num_points
            })

        return {'items': items}

    def get(self):
        r = requests.get(self.url)

        if r.status_code == 200 and len(r.content) > 0:
            return self._parse(r.content)
        return {}
