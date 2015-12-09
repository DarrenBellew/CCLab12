FROM python:2.7

# FILE author
MAINTAINER Islarf

# Update source
RUN apt-get update

# Upgrade the sources list
RUN apt-get -y upgrade

# copy app folder inside container
ADD /pythonApp /pythonApp

# Get pip(python thing) to download/install requirements
RUN pip install -r /pythonApp/requirements.txt

# Expose listener port
EXPOSE 5000

# Set the default directory where CMD will execute
WORKDIR /pythonApp

# when creating new container
CMD python server.py

