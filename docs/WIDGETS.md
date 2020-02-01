Available widgets
=================

Common options
--------------

All jobs have the following fields: `enabled`, `interval` and `job_impl`.

`enabled` should be `True` to enable the job. If the key is omitted or `False`,
the job won't be enabled.

`interval` specifies how often the job should run, in seconds. `interval` set to
`60` will make the job run every 60 seconds.

`job_impl` specifies which job implementation to use for this job. Valid job
implementations are the ones found in `jarvis/jobs/`, excluding the `.py`
extension. Specifying `job_impl` allows an implementation to be reused, it
defaults to the job key.

Most jobs also accept a `timeout` option. This option sets how long a job should
wait for a request to complete, in seconds. Timeout should be lower than
interval to prevent slow jobs from blocking future jobs.

atb
---
Displays bus routes in Trondheim, Norway. Uses the API provided by
[atbapi](https://github.com/mpolden/atbapi).

```python
JOBS['atb'] = {
    'enabled': True,
    'interval': 60,
    'url': 'https://atbapi.tar.io/api/v1/departures/<location-id>'
}
```

A list of possible location IDs is available here:
https://atbapi.tar.io/api/v1/busstops

avinor
------
Displays future flights for the configured destination. This widget uses
[data provided by Avinor](https://avinor.no/konsern/tjenester/flydata/flydata-i-xml-format).

```python
JOBS['avinor'] = {
    'enabled': True,
    'interval': 180,
    'from': 'TRD',
    'to': 'OSL'
}
```

The `from` and `to` fields are
[IATA airport codes](https://en.wikipedia.org/wiki/IATA_airport_code).

calendar
--------
Displays current and upcoming events in your Google Calendar. This widget uses
the Google Calendar API to retrieve data.

```python
JOBS['calendar'] = {
    'enabled': True,
    'interval': 600,
    'client_id': '',
    'client_secret': ''
}
```

The values for `client_id` and `client_secret` can be created using the
[Google Developer Console](https://code.google.com/apis/console/#:access).

When you have set `client_id` and `client_secret` in your config file, you need
to run `make google-api-auth` to generate a credentials file.

flybussen
---------
Displays the next [Flybussen](https://www.flybussen.no) departures from the
configured bus stop.

```python
JOBS['flybussen'] = {
    'enabled': True,
    'interval': 600,
    'from_stop': 'Dronningens gate D2',
    'to_airport': 'TRD'
}
```

The `from_stop` field is the name (case-insensitive) of a valid bus stop.

The `to_airport` field is a [IATA airport
code](https://en.wikipedia.org/wiki/IATA_airport_code) of a valid destination
airport.

See the [Flybussen website](https://www.flybussen.no) for valid airports and
stop names.

gmail
-----
Displays the current unread count, and total email count in the configured
folder.

```python
JOBS['gmail'] = {
    'enabled': True,
    'interval': 900,
    'client_id': '',
    'client_secret': '',
    'email': 'example@gmail.com',
    'folder': 'inbox'
}
```

The values for `client_id` and `client_secret` can be created using the
[Google Developer Console](https://code.google.com/apis/console/#:access).

When you have set `client_id` and `client_secret` in your config file, you need
to run `make google-api-auth` to generate a credentials file.

hackernews
----------
Displays the top 10 trending items on
[Hacker News](https://news.ycombinator.com/). Scrapes data directly from the
website.

```python
JOBS['hackernews'] = {
    'enabled': True,
    'interval': 900
}
```

imap
----------
Uses IMAP to display the current unread count, and total email count in the configured
folder.

```python
JOBS['imap'] = {
    'enabled': True,
    'interval': 900,
    'email': 'email-address-to-display,
    'url': 'imap://username:password@host:port',
    'tls': True,
    'starttls': False,
    'folder': 'INBOX'
}
```

nsb
---
Displays upcoming train departures from a configured location. Scrapes data
directly from https://www.nsb.no.

```python
JOBS['nsb'] = {
    'enabled': True,
    'interval': 900,
    'from': 'Lillehammer',
    'to': 'Oslo S'
}
```

The `from` and `to` fields are the same location names as used on the website.

ping
----
Displays a graph of response times to the given hosts. The `hosts` field is
a tuple of tuples on this format: `('label', 'host or ip')`

```python
JOBS['ping'] = {
    'enabled': True,
    'interval': 10,
    'hosts': (
        ('vg.no', 'vg.no'),
        ('google.com', 'google.com')
    )
}
```

Note that for this job the `timeout` parameter is applied per host, so the total
timeout is `timeout * len(hosts)`.

plex
----
Displays latest TV shows and movies from Plex Media Server. Plex Media Server
makes metadata for each section available as XML at the following URL:
`https://<ip>:32400/library/sections/<section-number>/recentlyAdded?X-Plex-Token=<secret-token>`.

```python
JOBS['plex'] = {
    'enabled': True,
    'interval': 900,
    'movies': 'https://127.0.0.1:32400/library/sections/2/recentlyAdded?X-Plex-Token=secret',
    'shows': 'https://127.0.0.1:32400/library/sections/1/recentlyAdded?X-Plex-Token=secret',
    'verify': True
}
```

Please see the
[Plex documentation](https://support.plex.tv/hc/en-us/articles/204059436-Finding-your-account-token-X-Plex-Token)
for instruction on how to find your token.

If `verify` is set to `False`, certificate warnings are ignored when using
HTTPS. Default is `True`.

rss
---
Displays the most recent items in a RSS feed. Works with any standard RSS feed.

```python
JOBS['rss-guardian'] = {
    'enabled': False,
    'interval': 900,
    'url': 'https://www.theguardian.com/international/rss',
    'title': 'The Guardian',
    'job_impl': 'rss'
}
```

The `title` field specifies the widget title. If it's omitted, the title will be
taken from `<title>` tag in the RSS feed.

sonos
-----
Displays the current track playing on your Sonos device. Also displays the
upcoming track.

```python
JOBS['sonos'] = {
    'enabled': False,
    'interval': 10,
    'ip': '127.0.0.1',
    'display_album_art': True
}
```

The `ip` field should be the IP of your Sonos device. If `display_album_art` is
`True` (default) the widget will use album art for the currently playing track
as its background image.

stats
-----
Displays beverage consumption stats from the IRC channel #tihlde on freenode.
The `max` dict sets the wanted limit for each beverage. `nick` is the nick you
want to retrieve stats for.

```python
JOBS['stats'] = {
    'enabled': True,
    'interval': 600,
    'nick': 'yournick',
    'max': {
        'coffee': 8,
        'beer': 12
    }
}
```

time
----
Displays the current time and date. This widget has no associated job and is not
configurable.

uptime
------
Ping one or more hosts and display their status (up or down).

```python
JOBS['uptime'] = {
    'enabled': True,
    'interval': 60,
    'hosts': (
        ('Desktop', '10.0.0.11'),
        ('Laptop', '10.0.0.10')
    )
}
```

Note that for this job the `timeout` parameter is applied per host, so the total
timeout is `timeout * len(hosts)`.

vaernesekspressen
---------
Displays the next [Vaernesekspressen](https://www.vaernesekspressen.no)
departures from the configured bus stop.

```python
JOBS['vaernesekspressen'] = {
    'enabled': True,
    'interval': 600,
    'from_stop': 'FB 73 Nidarosdomen'
}
```

The `from_stop` field is the name (case-insensitive) of a valid bus stop.

See the [Vaernesekspressen website](https://www.vaernesekspressen.no) for valid
stop names. Trondheim airport is the only possible destination and is thus not
configurable.

yr
--
Displays weather data from https://www.yr.no. The `url` field specifies the XML
feed to use. Note that Yr requires a polling interval of at least 10 minutes
(600 seconds).

```python
JOBS['yr'] = {
    'enabled': True,
    'interval': 600,
    'url': ('https://www.yr.no/sted/Norge/Tr%C3%B8ndelag/Trondheim/'
            'Trondheim/varsel.xml'),
    'forecast_fallback': True
}
```

Setting `forecast_fallback` to `True` (default) will display the weather
forecast in case the closest weather station is reporting incomplete data.
