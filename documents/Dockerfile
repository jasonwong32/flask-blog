FROM python:3.10-alpine

EXPOSE 5000

RUN apk update \
    && apk add gcc \
    && apk add musl-dev \
    && apk add linux-headers


WORKDIR /srv

COPY requirements.txt /srv/requirements.txt
COPY uwsgi.ini /uwsgi.ini
COPY app /srv

RUN pip install -r /srv/requirements.txt --no-cache-dir


CMD [ "uwsgi", "--ini","/uwsgi.ini" ]

