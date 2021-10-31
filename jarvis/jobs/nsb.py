# -*- coding: utf-8 -*-

import requests
from datetime import datetime
from jobs import AbstractJob


class Nsb(AbstractJob):
    def __init__(self, conf):
        self.from_location = conf["from"]
        self.to_location = conf["to"]
        self.interval = conf["interval"]
        self.timeout = conf.get("timeout")

    def _parse(self, json):
        date_format = "%Y-%m-%dT%H:%M:%S"
        departures = []
        for itinerary in json["itineraries"]:
            departure = datetime.strptime(itinerary["departureScheduled"], date_format)
            arrival = datetime.strptime(itinerary["arrivalScheduled"], date_format)
            duration = abs((arrival - departure).total_seconds())
            departures.append(
                {
                    "departure": departure.isoformat(),
                    "arrival": arrival.isoformat(),
                    "duration": duration,
                }
            )

        return {
            "from": self.from_location,
            "to": self.to_location,
            "departures": departures,
        }

    def get(self):
        now = datetime.now()
        data = {
            "from": self.from_location,
            "to": self.to_location,
            "time": now.strftime("%Y-%m-%dT%H:%M"),
        }
        url = "https://booking.cloud.nsb.no/api/itineraries/search"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; "
                "rv:93.0) Gecko/20100101 Firefox/93.0"
            )
        }
        r = requests.post(url, timeout=self.timeout, json=data, headers=headers)
        r.raise_for_status()
        return self._parse(r.json())
