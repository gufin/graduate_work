FROM python:3.10.7-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV DOCKERIZE_VERSION=v0.6.1

RUN apk update \
    && apk add \
       curl \
       postgresql-dev \
       postgresql-client \
       build-base \
       libxml2-dev \
       libxslt-dev \
       libffi-dev \
       jpeg-dev \
       freetype-dev

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz


COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

COPY ./src .

RUN chmod u+x /app/docker-entrypoint.sh
