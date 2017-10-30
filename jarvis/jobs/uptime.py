# -*- coding: utf-8 -*-

from jobs import AbstractJob
from subprocess import Popen, PIPE
from sys import platform


class Uptime(AbstractJob):

    def __init__(self, conf):
        self.hosts = conf['hosts']
        self.interval = conf['interval']
        self.timeout = conf.get('timeout')

    def _deadline_flag(self):
        if self.timeout is None:
            return []
        # ping on darwin uses -t for deadline/timeout
        if platform == 'darwin':
            return ['-t', str(self.timeout)]
        return ['-w', str(self.timeout)]

    def get(self):
        hosts = []
        for label, ip in self.hosts:
            ping_cmd = 'ping6' if ':' in ip else 'ping'
            ping = [ping_cmd, '-c', '1'] + self._deadline_flag() + [ip]
            p = Popen(ping, stdout=PIPE, stderr=PIPE)
            hosts.append({
                'label': label,
                'ip': ip,
                'active': p.wait() == 0
            })
        return {'hosts': hosts}
