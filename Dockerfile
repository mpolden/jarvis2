# Use base image (Ubuntu 12.10)
FROM base

# Install required system packages
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get install -y wget python-virtualenv python-dev libxml2-dev libxslt1-dev libyaml-dev

# Add files
RUN mkdir -p /app
ADD . /app

# Install pip dependencies
RUN pip install --use-mirrors -r /app/requirements.txt

# Expose app port
EXPOSE 5000

# Command for running app
CMD /app/app.py
