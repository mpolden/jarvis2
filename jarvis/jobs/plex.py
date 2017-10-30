# -*- coding: utf-8 -*-

import requests
from urllib3.exceptions import InsecureRequestWarning
from jobs import AbstractJob


class Plex(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']
        self.movies = conf['movies']
        self.shows = conf['shows']
        self.timeout = conf.get('timeout')
        self.verify = conf.get('verify', True)
        if not self.verify:
            requests.packages.urllib3.disable_warnings(
                category=InsecureRequestWarning
            )

    def _parse_movies(self, data):
        return [{'title': m.get('title'),
                 'year': m.get('year')}
                for m in data['MediaContainer']['Metadata']]

    def _parse_shows(self, data):
        return [{'title': s.get('title'),
                 'year': s.get('year'),
                 'name': s.get('grandparentTitle'),
                 'episode': '{0:02d}'.format(s.get('index')),
                 'season': '{0:02d}'.format(s.get('parentIndex'))}
                for s in data['MediaContainer']['Metadata']]

    def _get_json(self, url):
        headers = {'Accept': 'application/json'}
        r = requests.get(url, headers=headers, timeout=self.timeout,
                         verify=self.verify)
        r.raise_for_status()
        return r.json()

    def get(self):
        data = self._get_json(self.movies)
        movies = self._parse_movies(data)

        data = self._get_json(self.shows)
        shows = self._parse_shows(data)

        return {'movies': movies, 'shows': shows}
