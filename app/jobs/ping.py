#!/usr/bin/env python

import re
from datetime import datetime
from jobs import AbstractJob
from subprocess import Popen, PIPE


class Ping(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']
        self.hosts = conf['hosts']
        self.timeout = conf.get('timeout', 1)

    def _parse_time(self, ping_output):
        time = re.search(r'time=(\d+(?:\.\d+)?)', ping_output)
        return float(time.group(1)) if time is not None else 0

    def _get_latency(self, host):
        ping_cmd = 'ping6' if ':' in host else 'ping'
        ping = '%s -w %d -c 1 %s' % (ping_cmd, self.timeout, host)
        p = Popen(ping.split(' '), stdout=PIPE, stderr=PIPE)
        return self._parse_time(p.communicate()[0].decode())

    def get(self):
        values = []
        for label, host in self.hosts:
            latency = self._get_latency(host)
            now = datetime.now()
            values.append({
                'label': label,
                'host': host,
                'time': now.strftime('%H:%M:%S'),
                'latency': latency
            })
        return values
