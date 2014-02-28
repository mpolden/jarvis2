#!/usr/bin/env python

from jobs import AbstractJob
from subprocess import Popen, PIPE


class Uptime(AbstractJob):

    def __init__(self, conf):
        self.hosts = conf['hosts']
        self.interval = conf['interval']
        self.timeout = conf.get('timeout', 1)

    def get(self):
        for host in self.hosts:
            ping_cmd = 'ping6' if ':' in host['ip'] else 'ping'
            ping = '%s -w %d -c 1 %s' % (ping_cmd, self.timeout, host['ip'])
            p = Popen(ping.split(' '), stdout=PIPE, stderr=PIPE)
            host['active'] = p.wait() == 0
        return {'hosts': self.hosts}
