# -*- coding: utf-8 -*-

import imaplib
import re

try:
    # urlparse was moved to urllib.parse in Python 3
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
from jobs import AbstractJob


class IMAP(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']
        self.email = conf['email']
        self.url = urlparse(conf['url'])
        self.tls = conf.get('tls', True)
        self.starttls = conf.get('starttls', False)
        self.folder = conf['folder']

    def _parse_count(self, message):
        count = re.search(r'\w+ (\d+)', message.decode('utf-8'))
        return int(count.group(1)) if count is not None else 0

    def _get_count(self):
        _, message = self.mail.status(self.folder, '(MESSAGES)')
        return self._parse_count(message[0])

    def _get_unread_count(self):
        _, message = self.mail.status(self.folder, '(UNSEEN)')
        return self._parse_count(message[0])

    def get(self):
        if self.tls:
            self.mail = imaplib.IMAP4_SSL(self.url.hostname, self.url.port)
        else:
            self.mail = imaplib.IMAP4(self.url.hostname, self.url.port)
        if self.starttls:
            self.mail.starttls()
        self.mail.login(self.url.username, self.url.password)
        count = self._get_count()
        unread = self._get_unread_count()
        self.mail.logout()
        return {
            'email': self.email,
            'folder': self.folder,
            'count': count,
            'unread': unread
        }
