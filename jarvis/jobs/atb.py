# -*- coding: utf-8 -*-

import requests
from jobs import AbstractJob


class Atb(AbstractJob):

    def __init__(self, conf):
        self.url = conf['url']
        self.interval = conf['interval']
        self.timeout = conf.get('timeout')

    def get(self):
        r = requests.get(self.url, timeout=self.timeout)
        r.raise_for_status()
        return r.json()
