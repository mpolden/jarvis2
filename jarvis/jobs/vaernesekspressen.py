# -*- coding: utf-8 -*-

import json
import requests

from datetime import datetime, timedelta, timezone
from jobs import AbstractJob


class Vaernesekspressen(AbstractJob):
    def __init__(self, conf):
        self.from_stop = conf.get("from_stop")
        self.interval = conf["interval"]
        self.timeout = conf.get("timeout")
        self.base_url = conf.get("base_url", "https://unibussticket.azurewebsites.net")
        self.now = datetime.now
        if self.from_stop is None:
            raise ValueError("from_stop must be set")

    def _find_stop(self, now):
        today = now.strftime("%Y-%m-%d")
        url = f"{self.base_url}/api/operators/UNI:Operator:VerExp/lines/3/routes/8/stops?lang=no&date={today}"
        r = requests.get(url, timeout=self.timeout)
        r.raise_for_status()
        for stop in r.json():
            if stop["name"].lower() == self.from_stop.lower():
                return stop["id"], stop["name"]
        raise ValueError('Could not find ID for stop "{}"'.format(self.from_stop))

    def _departures(self, stop_id, stop_name, dt):
        url = f"{self.base_url}/api/operators/UNI:Operator:VerExp/lines/3/routes/8/departures"
        today = dt.strftime("%Y-%m-%d")
        data = {
            "from": str(stop_id),
            "to": "NSR:Quay:100211",  # Trondheim lufthavn
            "date": today,
            "type": "NORMAL",
            "travelers": json.dumps(
                [
                    {
                        "travellerProfileId": 1,
                        "maximumAge": 120,
                        "isAdult": True,
                        "name": "Voksen",
                        "count": 1,
                    }
                ]
            ),
        }
        r = requests.get(url, params=data, timeout=self.timeout)
        r.raise_for_status()
        departures = []
        for d in r.json():
            departure_time = datetime.fromisoformat(f"{today}T{d['time']}")
            departure = {
                "stop_name": stop_name,
                "destination_name": "Trondheim lufthavn",
                "departure_time": int(departure_time.timestamp()),
            }
            departures.append(departure)
        return departures

    def get(self):
        now = self.now()
        stop_id, stop_name = self._find_stop(now)
        departures = self._departures(stop_id, stop_name, now)
        if len(departures) < 2:
            # Few departures today, include tomorrow's departures
            tomorrow = (now + timedelta(days=1)).date()
            departures += self._departures(stop_id, stop_name, tomorrow)
        from_ = "N/A"
        to = "N/A"
        if len(departures) > 0:
            from_ = departures[0]["stop_name"]
            to = departures[0]["destination_name"]
        return {"from": from_, "to": to, "departures": departures}
