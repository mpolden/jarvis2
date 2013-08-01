#!/usr/bin/env python

from jobs import AbstractJob
from soco import SoCo


class Sonos(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']
        self.sonos = SoCo(conf['ip'])

    def get(self):
        try:
            current_track = self.sonos.get_current_track_info()
            next_track = self.sonos.get_queue(
                int(current_track['playlist_position']), 1).pop()
            return {
                'room': self.sonos.get_speaker_info()['zone_name'],
                'current': current_track,
                'next': next_track
            }
        except:
            return {}
