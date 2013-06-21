JARVIS v2
=========
A new and improved version of [JARVIS](https://github.com/martinp/jarvis)
(without that Ruby nonsense).

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

Screenshot
==========
![Screenshot](https://github.com/martinp/jarvis2/raw/master/public/jarvis2.png)
