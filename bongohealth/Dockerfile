# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/bongohealth

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy the project
COPY . .
