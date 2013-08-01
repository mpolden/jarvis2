#!/usr/bin/env python

import requests
from jobs import AbstractJob
from lxml import etree


class Plex(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']
        self.movies = conf['movies']
        self.shows = conf['shows']

    def get(self):
        r = requests.get(self.movies)
        movies_doc = etree.fromstring(r.content)

        r = requests.get(self.shows)
        shows_doc = etree.fromstring(r.content)

        data = {
            'movies': [],
            'shows': []
        }
        for movie in movies_doc.xpath('/MediaContainer/Video'):
            data['movies'].append({
                'title': movie.get('title'),
                'year': movie.get('year')
            })
        for show in shows_doc.xpath('/MediaContainer/Video'):
            data['shows'].append({
                'name': show.get('grandparentTitle'),
                'title': show.get('title'),
                'episode': show.get('index').zfill(2),
                'season': show.get('parentIndex').zfill(2)
            })
        return data
