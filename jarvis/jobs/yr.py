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

HOUR_OF_NEXT_DAY = 12


class Yr(AbstractJob):
    def __init__(self, conf):
        self.url = conf["url"]
        self.interval = conf["interval"]
        self.timeout = conf.get("timeout")
        self.location = conf.get("location")

    def _get_temperature(self, data):
        return data["data"]["instant"]["details"]["air_temperature"]

    def _get_description(self, data, period=None):
        if period is None:
            period = "next_1_hours"
        symbol_code = data["data"][period]["summary"]["symbol_code"]
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

    def _get_direction(self, deg):  # noqa: C901
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

    def _get_day_name(self, dt):
        day = dt.weekday()
        if day == 0:
            return "mandag"
        elif day == 1:
            return "tirsdag"
        elif day == 2:
            return "onsdag"
        elif day == 3:
            return "torsdag"
        elif day == 4:
            return "fredag"
        elif day == 5:
            return "lørdag"
        elif day == 6:
            return "søndag"
        raise ValueError("Invalid day: {}".format(day))

    def _get_wind(self, data):
        speed = data["data"]["instant"]["details"]["wind_speed"]
        direction = self._get_direction(
            data["data"]["instant"]["details"]["wind_from_direction"]
        )
        description = self._baufort(speed)
        return {"speed": speed, "direction": direction, "description": description}

    def _find_forecast(self, data, date, hourly=False, count=6):
        if not hourly:
            date = date.replace(hour=HOUR_OF_NEXT_DAY)
        forecast = []
        for n in range(1, count + 1):
            forecasted_date = date + timedelta(days=n)
            if hourly:
                forecasted_date = date + timedelta(hours=n)
            observation = self._find_observation(data, forecasted_date)
            time = datetime.strptime(observation["time"], "%Y-%m-%dT%H:%M:%SZ")
            temperature = observation["data"]["instant"]["details"]["air_temperature"]
            if not hourly or n == 1:
                # Only get description for next 6 hours if we're forecasting several
                # days or if this is the first forecast
                _, symbol = self._get_description(observation, period="next_6_hours")
            day_name = self._get_day_name(time)
            f = {
                "day": day_name,
                "hour": time.hour,
                "temperature": temperature,
                "symbol": symbol,
            }
            forecast.append(f)
        return forecast

    def _find_observation(self, data, date):
        date = date.replace(minute=0, second=0, microsecond=0)
        date_fmt = date.strftime("%Y-%m-%dT%H:%M:%SZ")
        timeseries = data["properties"]["timeseries"]
        for ts in timeseries:
            if ts["time"] != date_fmt:
                continue
            return ts
        raise ValueError("No observation found for time {}".format(date_fmt))

    def _parse_week(self, data, date):
        forecast = self._find_forecast(data, date)
        return {"forecast": forecast}

    def _parse_day(self, data, date):
        observation = self._find_observation(data, date)
        temperature = self._get_temperature(observation)
        description, symbol = self._get_description(observation)
        wind = self._get_wind(observation)
        forecast = self._find_forecast(data, date, hourly=True)
        return {
            "location": self.location,
            "description": description,
            "symbol": symbol,
            "temperature": temperature,
            "wind": wind,
            "forecast": forecast,
        }

    def _parse(self, data, date=None):
        if date is None:
            date = datetime.now()
        next_day = (date + timedelta(days=1)).replace(hour=HOUR_OF_NEXT_DAY)
        return {
            "today": self._parse_day(data, date),
            "tomorrow": self._parse_day(data, next_day),
            "week": self._parse_week(data, date),
        }

    def get(self):
        # Yr API requires a unique user agent
        # https://api.met.no/weatherapi/locationforecast/2.0/documentation#AUTHENTICATION
        headers = {"User-Agent": "jarvis2/1.0"}
        r = requests.get(self.url, timeout=self.timeout, headers=headers)
        r.raise_for_status()
        return self._parse(r.json())
