#!/bin/sh
python3 manage.py createsuperuser --noinput
python3 manage.py migrate
gunicorn -w 2 -b 0.0.0.0:8000 food.wsgi:application