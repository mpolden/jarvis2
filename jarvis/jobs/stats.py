# -*- coding: utf-8 -*-

import requests
from datetime import datetime
from jobs import AbstractJob


class Stats(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']
        self.nick = conf['nick']
        self.max = conf['max']
        self.timeout = conf.get('timeout')

    def get(self):
        today = datetime.now().date().strftime('%s000')
        params = {
            'q': 'statsByTimestamp(\'{nick}\', {today})'.format(nick=self.nick,
                                                                today=today)
        }
        r = requests.get('http://hilde.nerdvana.tihlde.org:3000',
                         timeout=self.timeout, params=params)
        r.raise_for_status()
        return {
            'stats': r.json(),
            'max': self.max,
            'nick': self.nick
        }
