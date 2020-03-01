# -*- coding: utf-8 -*-

from jobs import AbstractJob
from soco import SoCo


class Sonos(AbstractJob):

    def __init__(self, conf):
        self.interval = conf['interval']
        self.display_album_art = conf.get('display_album_art', True)
        self._device = SoCo(conf['ip'])
        self._timeout = conf.get('timeout')

    @property
    def timeout(self):
        if self._timeout is None:
            return None
        return (self._timeout, self._timeout)  # connect and read timeout

    @property
    def device(self):
        # In case of grouped devices the playback information needs to be
        # retrieved from the coordinator device
        if self._device.group.coordinator.uid != self._device.uid:
            self._device = self._device.group.coordinator
        return self._device

    def get(self):
        speaker_info = self.device.get_speaker_info(timeout=self.timeout)
        zone_name = speaker_info['zone_name']
        current_track = self.device.get_current_track_info()
        queue = self.device.get_queue()
        next_item = next(iter(queue), None)
        next_track = {}
        if next_item is not None:
            next_track = {
                'artist': next_item.creator,
                'title': next_item.title,
                'album': next_item.album
            }
        state = self.device.get_current_transport_info()[
            'current_transport_state']
        return {
            'room': zone_name,
            'state': state,
            'current': current_track,
            'next': next_track,
            'display_album_art': self.display_album_art
        }
