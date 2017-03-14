Deployment guide
================
JARVIS is a [Flask](http://flask.pocoo.org) application, see the
[uWSGI docs](http://uwsgi-docs.readthedocs.org/en/latest/WSGIquickstart.html)
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
    pip install --use-mirrors -r requirements.txt

Copy sample config and edit it to suit your needs:

    cp $APP_PATH/app/config.py.sample $APP_PATH/app/config.py

Create cache directories (needs to be writable by uwsgi process):

    mkdir -p $APP_PATH/app/static/{.webassets-cache,gen}
    chown www-data:www-data $APP_PATH/app/static/{.webassets-cache,gen}

Install nginx and uwsgi:

    aptitude install nginx uwsgi uwsgi-plugin-python

Configure app config in `/etc/uwsgi/apps-available/jarvis2.ini`:

    [uwsgi]
    workers = 1
    threads = 20
    plugin = python
    chdir = /path/to/jarvis2/app
    home = /path/to/jarvis2/venv
    env = JARVIS_SETTINGS=config.py
    module = main
    callable = app

Enable uwsgi app and start uwsgi:

    ln -s /etc/uwsgi/apps-available/jarvis2.ini /etc/uwsgi/apps-enabled/jarvis2.ini
    service uwsgi start

Configure nginx site in `/etc/nginx/sites-available/jarvis2`:

    server {
        location /static/ {
            alias /path/to/jarvis2/app/static/;
        }
        location / {
            include uwsgi_params;
            uwsgi_buffering off;
            uwsgi_pass unix:/tmp/uwsgi.sock;
        }
    }

Enable nginx site and (re)start nginx:

    ln -s /etc/nginx/sites-available/jarvis2 /etc/nginx/sites-enabled/jarvis2
    service nginx start
