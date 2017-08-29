#!/usr/bin/env python

from jobs import AbstractJob
from soco import SoCo


class Sonos(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']
        self.sonos = SoCo(conf['ip'])
        # In case of grouped devices the playback information needs to be
        # retrieved from the coordinator device
        if self.sonos.group.coordinator.uid != self.sonos.uid:
            self.sonos = self.sonos.group.coordinator

    def get(self):
        zone_name = self.sonos.get_speaker_info()['zone_name']
        np = self.sonos.get_current_track_info()

        current_track = np if np['playlist_position'] != '0' else None
        queue = self.sonos.get_queue(int(np['playlist_position']), 1)
        next_item = queue.pop() if len(queue) > 0 else None
        next_track = {}
        if next_item is not None:
            next_track = {
                'artist': next_item.creator,
                'title': next_item.title,
                'album': next_item.album
            }

        state = self.sonos.get_current_transport_info()[
            'current_transport_state']

        return {
            'room': zone_name,
            'state': state,
            'current': current_track,
            'next': next_track
        }
