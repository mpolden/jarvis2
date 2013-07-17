JARVIS v2
=========
JARVIS is a dashboard framework designed to run on the Raspberry Pi.

The framework is written in Python and is a new and improved version of the old
[JARVIS](https://github.com/martinp/jarvis) project.

Screenshots
==========
![Screenshot 1](https://github.com/martinp/jarvis2/raw/master/public/jarvis2.png)
![Screenshot 2](https://github.com/martinp/jarvis2/raw/master/public/jarvis2_1.png)

Dependencies
============
JARVIS requires Python 2.6+ to run.

Some dependencies have native bindings which requires these packages on
Debian/Ubuntu:

    aptitude install -y python-dev libxml2-dev libxslt1-dev

Install Python packages:

    pip install --use-mirrors -r requirements.txt

For development it's recommended to use [virtualenv](http://www.virtualenv.org).

Development dependencies require [node.js](http://nodejs.org) and can be
installed with `npm install`. These are *not* required to run the app.

Configuration
=============
All configuration of widgets is done in a single Python source file. The
configuration is specified by setting the `JARVIS_SETTINGS` environment
variable.

A sample config (`app/config.py.sample`) is provided. This file can be used as a
starting point for your own configuration.

Copy `config.py.sample` to `config.py` and edit it to suit your needs.

Usage
=====
After installing dependencies and creating a config file, the app can be started
by running:

    JARVIS_SETTINGS=config.py ./run.py

To start the app in debug mode, use:

    JARVIS_SETTINGS=config.py ./run.py debug

Run a job standalone and pretty-print output (useful for debugging):

    JARVIS_SETTINGS=config.py make run-job

Create Google API credentials (required for Calendar widget):

    JARVIS_SETTINGS=config.py make google-api-auth

Create a new widget:

    make widget

Development environment
=======================
A `Vagrantfile` is included for use with [Vagrant](http://www.vagrantup.com).
Run `vagrant up` in the repository root to provision a development environment.

Deploying using Docker
======================
A experimental `Dockerfile` is included for use with
[Docker](http://www.docker.io).

A production-ready image can be built with `docker build -t jarvis2 $PWD` and
then using `docker run -t jarvis2` to run the app.

Deployment guide using nginx and uWSGI
======================================
JARVIS is a [Flask](http://flask.pocoo.org) application, see the
[uWSGI docs](http://uwsgi-docs.readthedocs.org/en/latest/WSGIquickstart.html)
for a more detailed uWSGI deployment guide or check out the other deployment
options described in the [Flask docs](http://flask.pocoo.org/docs/deploying)

This guide assumes Debian or Ubuntu, but most steps should work for other
distros.

Clone repo:

    export APP_PATH=/path/to/jarvis2
    git clone https://github.com/martinp/jarvis2.git $APP_PATH

Create virtualenv and install dependencies:

    cd $APP_PATH
    virtualenv venv
    source venv/bin/active
    pip install --use-mirrors -r requirements.txt

Copy sample config and edit it to suit your needs:

    cp $APP_PATH/app/config.py.sample $APP_PATH/app/config.py

Create cache directories (needs to be writable by uwsgi process):

    mkdir -p $APP_PATH/app/static/{.webassets-cache,assets}
    chown www-data:www-data $APP_PATH/app/static/{.webassets-cache,assets}

Install nginx and uwsgi:

    aptitude install nginx uwsgi uwsgi-plugin-python

Configure app config in `/etc/uwsgi/apps-available/jarvis2.ini`:

    [uwsgi]
    workers = 1
    threads = 20
    plugin = python
    chdir = /path/to/jarvis2
    home = /path/to/jarvis2/venv
    env = JARVIS_SETTINGS=config.py
    module = app.main
    callable = app

Enable uwsgi app and start uwsgi:

    ln -s /etc/uwsgi/apps-available/jarvis2.ini /etc/uwsgi/apps-enabled/jarvis2.ini
    service uwsgi start

Configure nginx site in `/etc/nginx/sites-available/jarvis2`:

    server {
        location / {
            try_files $uri @jarvis2;
        }
        location @jarvis2 {
            include uwsgi_params;
            uwsgi_buffering off;
            uwsgi_pass unix:/tmp/uwsgi.sock;
        }
        location /static {
            alias /path/to/jarvis2/app/static/;
        }
    }

Enable nginx site and (re)start nginx:

    ln -s /etc/nginx/sites-available/jarvis2 /etc/nginx/sites-enabled/jarvis2
    service nginx start
