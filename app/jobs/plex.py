#!/usr/bin/env python

import requests
from jobs import AbstractJob
from lxml import etree


class Plex(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']
        self.movies = conf['movies']
        self.shows = conf['shows']

    def _parse_movies(self, xml):
        tree = etree.fromstring(xml)
        movies = []
        for movie in tree.xpath('/MediaContainer/Video'):
            movies.append({
                'title': movie.get('title'),
                'year': movie.get('year')
            })
        return movies

    def _parse_shows(self, xml):
        tree = etree.fromstring(xml)
        shows = []
        for show in tree.xpath('/MediaContainer/Video'):
            shows.append({
                'name': show.get('grandparentTitle'),
                'title': show.get('title'),
                'episode': show.get('index').zfill(2),
                'season': show.get('parentIndex').zfill(2)
            })
        return shows

    def get(self):
        try:
            r = requests.get(self.movies)
            movies = self._parse_movies(r.content)

            r = requests.get(self.shows)
            shows = self._parse_shows(r.content)

            return {'movies': movies, 'shows': shows}
        except requests.exceptions.ConnectionError:
            return {}
