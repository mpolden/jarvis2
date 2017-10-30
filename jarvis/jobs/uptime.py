# -*- coding: utf-8 -*-

from jobs import AbstractJob
from subprocess import Popen, PIPE
from sys import platform


class Uptime(AbstractJob):

    def __init__(self, conf):
        self.hosts = conf['hosts']
        self.interval = conf['interval']
        self.timeout = conf.get('timeout', 1)

    def get(self):
        hosts = []
        for label, ip in self.hosts:
            ping_cmd = 'ping6' if ':' in ip else 'ping'
            deadline_flag = '-w'
            # ping on darwin uses -t for deadline/timeout
            if platform == 'darwin':
                deadline_flag = '-t'
            ping = '%s %s %d -c 1 %s' % (ping_cmd, deadline_flag, self.timeout,
                                         ip)
            p = Popen(ping.split(' '), stdout=PIPE, stderr=PIPE)
            hosts.append({
                'label': label,
                'ip': ip,
                'active': p.wait() == 0
            })
        return {'hosts': hosts}
