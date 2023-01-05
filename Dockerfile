FROM python:3.10-buster

EXPOSE 5000



WORKDIR /srv

COPY requirements.txt /srv/requirements.txt
RUN pip install -r /srv/requirements.txt --no-cache-dir

COPY api /srv/app/api
COPY app.py /srv/app
COPY .env /srv/app
COPY config.py /srv/app

CMD ["gunicorn","-w 4", "--bind 0.0.0.0:8000", "wsgi:app" ]
