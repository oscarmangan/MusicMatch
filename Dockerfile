##
## Dockerfile to generate a Docker image of the project
##

# Start from an existing image with Python 3.8 installed
FROM python:3.8

MAINTAINER Oscar Mangan

# Run a series of Linux commands to ensure that
# 1. Everything is up-to-date and
# 2. Install GDAL
RUN apt-get -y update && apt-get -y upgrade && apt-get -y install libgdal-dev

# Make a working directory in the image and set it as working dir.
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# make sure that pip & setuptools are installed and to date
RUN pip install --upgrade pip setuptools wheel

# Get the following libraries. We caan install them "globally" on the image as it will contain only our project
RUN apt-get -y install build-essential python-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

# You should have already exported your Python library reuirements to a "requiremnts.txt" file using pip.
# Now copy this to the image and install everything in it.
COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt

# Copy everything in your Django project to the image.
COPY . /usr/src/app

# Make sure that static files are up to date and available
RUN python manage.py collectstatic --no-input

# Expose port 8000 on the image. We'll map a localhost port to this later.
EXPOSE 8001

# Run "uwsgi". uWSGI is a Web Server Gateway Interface (WSGI) server implementation that is typically used to run Python
# web applications
CMD ["uwsgi", "--ini", "uwsgi.ini"]
