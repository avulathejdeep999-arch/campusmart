#!/bin/sh
set -e
python manage.py migrate --noinput
python manage.py seed_listings ${SEED_ARGS}
exec gunicorn campusmart.wsgi:application --bind 0.0.0.0:8000 --workers 2
