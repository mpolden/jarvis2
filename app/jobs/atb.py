#!/usr/bin/env python

import requests
from jobs import AbstractJob


class Atb(AbstractJob):

    def __init__(self, conf):
        self.url = conf['url']
        self.interval = conf['interval']

    def get(self):
        r = requests.get(self.url)

        if r.status_code == 200 and len(r.content) > 0:
            return r.json()
        return {}
