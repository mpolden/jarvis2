# Use base image (Ubuntu 12.10)
FROM base

# Install required system packages
ENV DEBIAN_FRONTEND noninteractive
RUN echo "deb http://no.archive.ubuntu.com/ubuntu quantal main universe multiverse" > /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y wget python-pip python-dev libxml2-dev libxslt1-dev

# Time zone
RUN echo "Europe/Oslo" > /etc/timezone
RUN dpkg-reconfigure tzdata

# Add files
RUN mkdir /app
ADD ./app /app/app
ADD ./run.py /app/run.py
ADD ./requirements.txt /app/requirements.txt

# Install pip dependencies
RUN pip install --use-mirrors -r /app/requirements.txt

# Expose app port
EXPOSE 5000

# Command for running app
CMD JARVIS_SETTINGS="config.py" /app/run.py
