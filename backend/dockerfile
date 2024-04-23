# Pull base image
FROM python:3.11-slim

# Upgrade Base (Debian) Dependencies
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y --no-install-recommends \
	build-essential gcc

# Set environment variables
ENV python -m pip install --upgrade pip wheel setuptools
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY ./api ./api
COPY ./backend ./backend
COPY ./manage.py ./manage.py