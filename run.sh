#!/bin/sh
python ./manage.py migrate
python ./manage.py createsuperuser --noinput
gunicorn -w 2 -b 0.0.0.0:8000 graduation_project.wsgi:application
# python manage.py runserver 0.0.0.0:8000