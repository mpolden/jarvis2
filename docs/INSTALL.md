Deployment guide
================
JARVIS is a [Flask](http://flask.pocoo.org) application, see the
[uWSGI docs](https://uwsgi-docs.readthedocs.org/en/latest/WSGIquickstart.html)
for a more detailed uWSGI deployment guide or check out the other deployment
options described in the [Flask docs](http://flask.pocoo.org/docs/deploying)

This guide assumes Debian or Ubuntu, but most steps should work for other
distros.

Clone repo:

    export APP_PATH=/path/to/jarvis2
    git clone https://github.com/mpolden/jarvis2.git $APP_PATH

Create virtualenv and install dependencies:

    cd $APP_PATH
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

Copy sample config and edit it to suit your needs:

    cp $APP_PATH/jarvis/config.py.sample $APP_PATH/jarvis/config.py

Create cache directories (needs to be writable by uwsgi process):

    mkdir -p $APP_PATH/jarvis/static/{.webassets-cache,gen}
    chown www-data:www-data $APP_PATH/jarvis/static/{.webassets-cache,gen}

Install nginx and uwsgi:

    aptitude install nginx uwsgi uwsgi-plugin-python

Configure app config in `/etc/uwsgi/apps-available/jarvis.ini`:

    [uwsgi]
    workers = 1
    threads = 20
    plugin = python
    chdir = /path/to/jarvis2/jarvis
    home = /path/to/jarvis2/venv
    env = JARVIS_SETTINGS=config.py
    module = app
    callable = app

Enable uwsgi app and start uwsgi:

    ln -s /etc/uwsgi/apps-available/jarvis.ini /etc/uwsgi/apps-enabled/jarvis.ini
    systemctl restart uwsgi

Configure nginx site in `/etc/nginx/sites-available/jarvis`:

    server {
        location /static/ {
            alias /path/to/jarvis2/jarvis/static/;
        }
        location / {
            include uwsgi_params;
            uwsgi_buffering off;
            uwsgi_pass unix:/run/uwsgi/app/jarvis/socket;
        }
    }

Enable nginx site and (re)start nginx:

    ln -s /etc/nginx/sites-available/jarvis /etc/nginx/sites-enabled/jarvis
    systemctl restart nginx
