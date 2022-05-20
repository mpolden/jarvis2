# -*- coding: utf-8 -*-

import requests
from datetime import datetime
from jobs import AbstractJob


class Nsb(AbstractJob):
    def __init__(self, conf):
        self.from_stop_id, self.from_location = conf["from"]
        self.to_stop_id, self.to_location = conf["to"]
        self.interval = conf["interval"]
        self.timeout = conf.get("timeout")

    def _parse(self, json):
        departures = []
        for tp in json["data"]["trip"]["tripPatterns"]:
            legs = tp["legs"]
            if len(legs) == 0:
                continue
            elif len(legs) > 1:
                raise ValueError("found {} legs, but expected 1".format(len(legs)))
            departure = datetime.fromisoformat(legs[0]["expectedStartTime"])
            arrival = datetime.fromisoformat(legs[0]["expectedEndTime"])
            duration = tp["duration"]
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
        query = """
{
  trip(
    from: {
      place: "NSR:StopPlace:%d"
    },
    to: {
      place: "NSR:StopPlace:%d"
    },
    modes: {
      transportModes: {
        transportMode: rail
      }
    },
    searchWindow: 720,
    maximumTransfers: 1
  ) {
    tripPatterns {
      duration
      legs {
        expectedStartTime
        expectedEndTime
        line {
          id
          publicCode
        }
      }
    }
  }
}
"""
        data = {"query": query % (self.from_stop_id, self.to_stop_id)}
        url = "https://api.entur.io/journey-planner/v3/graphql"
        headers = {"ET-Client-Name": "github_mpolden-jarvis2"}
        r = requests.post(url, timeout=self.timeout, json=data, headers=headers)
        r.raise_for_status()
        return self._parse(r.json())
