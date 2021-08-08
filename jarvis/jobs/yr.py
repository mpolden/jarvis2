# -*- coding: utf-8 -*-

import requests
from datetime import datetime, timedelta
from jobs import AbstractJob

SYMBOL_TABLE = {
    "sleetshowersandthunder": "Sluddbyger og torden",
    "heavyrainandthunder": "Kraftig regn og torden",
    "partlycloudy": "Delvis skyet",
    "rainshowersandthunder": "Regnbyger og torden",
    "lightssnowshowersandthunder": "Lette snøbyger og torden",
    "sleet": "Sludd",
    "lightsleetandthunder": "Lett sludd og torden",
    "lightsleetshowers": "Lette sluddbyger",
    "lightrain": "Lett regn",
    "lightsnow": "Lett snø",
    "lightrainshowers": "Lette regnbyger",
    "heavysnowshowers": "Kraftige snøbyger",
    "lightrainandthunder": "Lett regn og torden",
    "heavysnow": "Kraftig snø",
    "heavysleet": "Kraftig sludd",
    "lightsnowandthunder": "Lett snø og torden",
    "heavysleetshowers": "Kraftige sluddbyger",
    "fair": "Lettskyet",
    "snowshowers": "Snøbyger",
    "heavysnowandthunder": "Kraftig snø og torden",
    "heavyrainshowersandthunder": "Kraftige regnbyger og torden",
    "fog": "Tåke",
    "heavyrain": "Kraftig regn",
    "snowshowersandthunder": "Snøbyger og torden",
    "lightssleetshowersandthunder": "Lette sluddbyger og torden",
    "clearsky": "Klarvær",
    "rainshowers": "Regnbyger",
    "cloudy": "Skyet",
    "heavysnowshowersandthunder": "Kraftige snøbyger og torden",
    "heavysleetandthunder": "Kraftig sludd og torden",
    "snow": "Snø",
    "rainandthunder": "Regn og torden",
    "sleetandthunder": "Sludd og torden",
    "lightsleet": "Lett sludd",
    "lightrainshowersandthunder": "Lette regnbyger og torden",
    "snowandthunder": "Snø og torden",
    "rain": "Regn",
    "heavyrainshowers": "Kraftige regnbyger",
    "lightsnowshowers": "Lette snøbyger",
    "sleetshowers": "Sluddbyger",
    "heavysleetshowersandthunder": "Kraftige sluddbyger og torden",
}

DEFAULT_FORECAST_HOUR = 12


class Yr(AbstractJob):
    def __init__(self, conf):
        self.url = conf["url"]
        self.interval = conf["interval"]
        self.location = conf["location"]
        self.timeout = conf.get("timeout")
        self.forecast_hour = conf.get("forecast_hour", DEFAULT_FORECAST_HOUR)

    def _temperature(self, observation):
        return observation["data"]["instant"]["details"]["air_temperature"]

    def _description(self, observation, short_term=True):
        # The periods returned from the Yr API are unpredicatable, we therefore try all
        # possible periods in order
        if short_term:
            periods = ("next_1_hours", "next_6_hours", "next_12_hours")
        else:
            periods = ("next_6_hours", "next_1_hours", "next_12_hours")
        known_periods = observation["data"].keys()
        period = next((p for p in periods if p in known_periods), None)
        if period is None:
            raise ValueError(
                "Yr API returned periods {}, which does not contain any of {}".format(
                    known_periods, periods
                )
            )
        symbol_code = observation["data"][period]["summary"]["symbol_code"]
        # Remove any trailing time of day identifier: cloudy_night -> cloudy
        symbol_key = symbol_code.split("_")[0]
        return (SYMBOL_TABLE[symbol_key], symbol_code)

    def _baufort(self, wind_speed):  # noqa: C901
        if wind_speed < 0.3:
            return "Stille"
        elif wind_speed < 1.6:
            return "Flau vind"
        elif wind_speed < 3.4:
            return "Svak vind"
        elif wind_speed < 5.5:
            return "Lett bris"
        elif wind_speed < 8.0:
            return "Laber bris"
        elif wind_speed < 10.8:
            return "Frisk bris"
        elif wind_speed < 13.9:
            return "Liten kuling"
        elif wind_speed < 17.2:
            return "Stiv kuling"
        elif wind_speed < 20.8:
            return "Sterk kuling"
        elif wind_speed < 24.5:
            return "Liten storm"
        elif wind_speed < 28.5:
            return "Full storm"
        elif wind_speed < 32.7:
            return "Sterk storm"
        return "Orkan"

    def _direction(self, deg):  # noqa: C901
        if deg <= 22.5 or deg > 337.5:
            return "nord"
        elif deg <= 67.5:
            return "nordøst"
        elif deg <= 112.5:
            return "øst"
        elif deg <= 157.5:
            return "sørøst"
        elif deg <= 202.5:
            return "sør"
        elif deg <= 247.5:
            return "sørvest"
        elif deg <= 292.5:
            return "vest"
        elif deg <= 337.5:
            return "nordvest"
        raise ValueError("Invalid direction {}".format(deg))

    def _wind(self, observation):
        speed = observation["data"]["instant"]["details"]["wind_speed"]
        direction = self._direction(
            observation["data"]["instant"]["details"]["wind_from_direction"]
        )
        description = self._baufort(speed)
        return {"speed": speed, "direction": direction, "description": description}

    def _find_forecast(self, data, date, hourly=False, count=6):
        if not hourly:
            date = date.replace(hour=self.forecast_hour)
        forecast = []
        for n in range(1, count + 1):
            forecasted_date = date + timedelta(days=n)
            if hourly:
                forecasted_date = date + timedelta(hours=n)
            observation = self._find_observation(data, forecasted_date)
            temperature = self._temperature(observation)
            if not hourly or n == 1:
                # Get the description for next 6 hours if we're forecasting future days
                # or if we're looking at the forecast for the first hour
                _, symbol = self._description(observation, short_term=False)
            f = {
                "time": observation["time"],
                "temperature": temperature,
                "symbol": symbol,
            }
            forecast.append(f)
        return forecast

    def _find_observation(self, data, date):
        date_fmt = date.strftime("%Y-%m-%dT%H:00:00Z")
        timeseries = data["properties"]["timeseries"]
        for ts in timeseries:
            if ts["time"] != date_fmt:
                continue
            return ts
        if date.hour != DEFAULT_FORECAST_HOUR:
            # Fall back to default hour if there is no match for given hour
            date = date.replace(hour=DEFAULT_FORECAST_HOUR)
            return self._find_observation(data, date)
        raise ValueError("No observation found for time {}".format(date_fmt))

    def _parse_week(self, data, date):
        forecast = self._find_forecast(data, date)
        return {"forecast": forecast}

    def _parse_day(self, data, date):
        observation = self._find_observation(data, date)
        forecast = self._find_forecast(data, date, hourly=True)
        temperature = self._temperature(observation)
        description, symbol = self._description(observation)
        wind = self._wind(observation)
        return {
            "location": self.location,
            "description": description,
            "symbol": symbol,
            "temperature": temperature,
            "wind": wind,
            "forecast": forecast,
        }

    def _parse(self, data, now=None):
        if now is None:
            now = datetime.utcnow()
        next_day = (now + timedelta(days=1)).replace(hour=self.forecast_hour)
        return {
            "today": self._parse_day(data, now),
            "tomorrow": self._parse_day(data, next_day),
            "week": self._parse_week(data, now),
        }

    def get(self):
        # Yr API requires a unique user agent
        # https://api.met.no/weatherapi/locationforecast/2.0/documentation#AUTHENTICATION
        headers = {"User-Agent": "jarvis2/1.0 (+https://github.com/mpolden/jarvis2)"}
        r = requests.get(self.url, timeout=self.timeout, headers=headers)
        r.raise_for_status()
        return self._parse(r.json())
