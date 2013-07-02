JARVIS v2
=========
A new and improved version of [JARVIS](https://github.com/martinp/jarvis)
(without that Ruby nonsense).

Screenshot
==========
![Screenshot](https://github.com/martinp/jarvis2/raw/master/public/jarvis2.png)

Dependencies
============
Use `pip install -r requirements.txt` to install dependencies. For development
it's recommended to use [virtualenv](http://www.virtualenv.org).

Development dependencies can be installed with `npm install`. These are *not*
required to run the app.

Configuration
=============
TODO

Usage
=====
After installing dependencies using `pip`, the app can be started by running

    ./run.py

To start the app in debug mode, use

    ./run.py debug

Deploying using Docker
======================
An experimental `Dockerfile` is included for use with
[Docker](http://www.docker.io).

A production-ready image can be built with `docker build -t jarvis2 $PWD` and
then using `docker run -t jarvis2` to run the app.

Deployment guide using nginx and uwsgi
======================================

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
    uid = www-data
    gid = www-data
    socket = /tmp/uwsgi.sock
    plugin = python
    home = /path/to/jarvis2/venv
    module = app.main
    callable = app
    chdir = /path/to/jarvis2
    env = JARVIS_SETTINGS=config.py
    workers = 1
    threads = 20

Enable uwsgi app and start uwsgi:

    ln -s /etc/uwsgi/apps-available/jarvis2.ini /etc/uwsgi/apps-enabled/jarvis2.ini
    service uwsgi start

Configure nginx site in `/etc/nginx/sites-available/jarvis2`:

    server {
        server_name localhost;
        location / { try_files $uri @jarvis2; }
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
