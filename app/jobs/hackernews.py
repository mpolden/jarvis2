#!/usr/bin/env python

import requests
from jobs import AbstractJob
from pyquery import PyQuery as pq


class HackerNews(AbstractJob):

    def __init__(self, conf):
        self.url = 'https://news.ycombinator.com'
        self.interval = conf['interval']
        self.timeout = conf.get('timeout')

    def _parse(self, html):
        d = pq(html)

        titles = [el.text for el in
                  d.find('td.title a')
                  .not_('a[href^="from"]')  # Source link
                  .not_('a[rel="nofollow"]')]  # "More" link

        points = [int(el.text.rstrip(' points')) for el in
                  d.find('td.subtext span.score')]

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
        return self._parse(r.content)
