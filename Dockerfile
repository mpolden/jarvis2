FROM ubuntu:15.04

ENV DEBIAN_FRONTEND noninteractive

ADD . /app

RUN apt-get -q update && \
    apt-get install -y wget python-pip build-essential python-dev libxml2-dev libxslt1-dev zlib1g-dev && \
    cp /app/app/config.py.sample /app/app/config.py && \
    pip install --use-mirrors -r /app/requirements.txt && \
    echo "Europe/Oslo" > /etc/timezone && \
    dpkg-reconfigure tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

VOLUME /app

EXPOSE 5000

WORKDIR /app

ENTRYPOINT JARVIS_SETTINGS=config.py make run