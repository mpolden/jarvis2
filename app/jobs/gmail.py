#!/usr/bin/env python

import imaplib
import re
from jobs import AbstractJob


class Gmail(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']
        self.email = conf['email']
        self.password = conf['password']
        self.folder = conf['folder']

    def _parse_count(self, message):
        count = re.search('\w+ (\d+)', message)
        return int(count.group(1)) if count is not None else 0

    def _get_count(self):
        _, message = self.mail.status(self.folder, '(MESSAGES)')
        return self._parse_count(message[0])

    def _get_unread_count(self):
        _, message = self.mail.status(self.folder, '(UNSEEN)')
        return self._parse_count(message[0])

    def get(self):
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        self.mail.login(self.email, self.password)
        count = self._get_count()
        unread = self._get_unread_count()
        self.mail.logout()
        return {
            'email': self.email,
            'folder': self.folder,
            'count': count,
            'unread': unread
        }
