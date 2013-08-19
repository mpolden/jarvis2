#!/usr/bin/env python

import requests
from datetime import datetime
from jobs import AbstractJob


class Stats(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']
        self.nick = conf['nick']
        self.max = conf['max']

    def get(self):
        today = datetime.now().date().strftime('%s000')
        params = {
            'q': 'statsByTimestamp(\'{nick}\', {today})'.format(nick=self.nick,
                                                                today=today)
        }
        r = requests.get('http://test.eirikb.no:3000', params=params)
        if r.status_code == 200 and len(r.content) > 0:
            return {
                'stats': r.json(),
                'max': self.max,
                'nick': self.nick
            }
        return {}
