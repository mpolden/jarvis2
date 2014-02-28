#!/usr/bin/env python

import requests

from pyquery import PyQuery as pq

from jobs import AbstractJob


class Steam(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']
        self.timeout = conf.get('timeout')

    def _parse(self, html):
        d = pq(html)

        deals = []
        elements = d.find('.wintersale_dailydeals .wintersale_dailydeal')
        for el in map(pq, elements):
            img = el.find('.dailydeal_cap').attr['src']
            percent = el.find('.discount_pct').text()
            original_price = el.find('.discount_original_price').text()
            final_price = el.find('.discount_final_price').text()
            deals.append(dict(img=img, percent=percent,
                              original_price=original_price,
                              final_price=final_price))
        return {'deals': deals}

    def get(self):
        r = requests.get('http://store.steampowered.com/',
                         timeout=self.timeout)
        if r.status_code == 200 and len(r.content) > 0:
            return self._parse(r.content)
        return {}
