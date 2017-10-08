#!/usr/bin/env python

from jobs import AbstractJob


class Mock(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']

    def get(self):
        return {'data': 'spam'}
