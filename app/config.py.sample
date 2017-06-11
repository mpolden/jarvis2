# Main configuration file for jarvis2
#
# Please see WIDGETS.md for more detailed documentation.

JOBS = {}

JOBS['yr'] = {
    # Enable job
    'enabled': True,
    # Run job every N seconds
    'interval': 600,
    # URL for data
    'url': ('https://www.yr.no/sted/Norge/S%C3%B8r-Tr%C3%B8ndelag/Trondheim/'
            'Trondheim/varsel.xml'),
    # Job timeout in seconds
    'timeout': 5
}

JOBS['time'] = {
    'enabled': True
}

JOBS['atb'] = {
    'enabled': True,
    'interval': 60,
    'url': 'https://atbapi.tar.io/api/v1/departures/16011376',
    'timeout': 5
}

# Add additional atb job for another departure
JOBS['atb-16010382'] = {
    'enabled': True,
    'interval': 60,
    'url': 'https://atbapi.tar.io/api/v1/departures/16010382',
    'timeout': 5,
    'job_name': 'atb'
}

JOBS['hackernews'] = {
    'enabled': True,
    'interval': 900,
    'timeout': 5
}

JOBS['sonos'] = {
    'enabled': False,
    'interval': 10,
    'ip': 'ip.addr',
    'timeout': 5
}

JOBS['calendar'] = {
    'enabled': False,
    'interval': 600,
    'client_id': '',
    'client_secret': '',
    'timeout': 5
}

JOBS['uptime'] = {
    'enabled': False,
    'interval': 60,
    'hosts': [
        ('Router', 'ip.addr'),
        ('Laptop', 'ip.addr')
    ],
    'timeout': 5
}

JOBS['plex'] = {
    'enabled': False,
    'interval': 900,
    'movies': 'https://ip:port/library/sections/2/recentlyAdded/',
    'shows': 'https://ip:port/library/sections/1/recentlyAdded/',
    'verify': False,
    'timeout': 5
}

JOBS['nsb'] = {
    'enabled': True,
    'interval': 900,
    # See https://nsb.no for valid locations
    'from': 'Trondheim S',
    'to': 'Oslo S',
    'timeout': 10
}

JOBS['ping'] = {
    'enabled': False,
    'interval': 3,
    'hosts': [
        ('google.com', 'google.com'),
        ('gw', '10.0.0.1')
    ],
    'timeout': 1
}

JOBS['gmail'] = {
    'enabled': False,
    'interval': 600,
    'email': 'your.username@gmail.com',
    'folder': 'inbox'
}

JOBS['imap'] = {
    'enabled': False,
    'interval': 600,
    'email': 'email-address-to-display',
    'url': 'imap://username:password@host:port',
    'tls': True,
    'starttls': False,
    'folder': 'INBOX'
}

JOBS['avinor'] = {
    'enabled': True,
    'interval': 180,
    'from': 'TRD',
    'to': 'OSL',
    'timeout': 5
}

JOBS['stats'] = {
    'enabled': False,
    'interval': 600,
    'nick': 'nick',
    'max': {
        'coffee': 8,
        'beer': 10
    },
    'timeout': 5
}

JOBS['stockquotes'] = {
    'enabled': True,
    'interval': 900,
    'symbols': [
        'YHOO',
        'AAPL',
        'GOOG',
        'MSFT'
    ]
}
