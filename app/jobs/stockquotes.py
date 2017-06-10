#!/usr/bin/env python

import requests

from jobs import AbstractJob


class Stockquotes(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']
        self.timeout = conf.get('timeout', 5)
        self.symbols = conf['symbols']

    def _build_query(self):
        symbols = '","'.join(self.symbols)
        q = 'select * from yahoo.finance.quotes where symbol in ("{}")'.format(
            symbols)
        return q

    def _parse(self, data):
        return [dict(symbol=q['Symbol'],
                     ask=q['Ask'],
                     change=q['Change'],
                     percent_change=q['PercentChange'])
                for q in data['query']['results']['quote']]

    def get(self):
        params = {
            'q': self._build_query(),
            'format': 'json',
            'env': 'store://datatables.org/alltableswithkeys'
        }
        r = requests.get('https://query.yahooapis.com/v1/public/yql',
                         timeout=self.timeout, params=params)
        r.raise_for_status()
        return self._parse(r.json())
