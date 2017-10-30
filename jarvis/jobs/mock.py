# -*- coding: utf-8 -*-

from jobs import AbstractJob


# This job is used in unit tests and does nothing useful
class Mock(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']

    def get(self):
        return {'data': 'spam'}
