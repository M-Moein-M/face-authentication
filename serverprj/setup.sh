#! /bin/bash

# add installation of django & drf

apt update
apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl

# create databse

# install python packages
pip install django gunicorn psycopg2-binary
pip install notificationapi_python_server_sdk
pip install python-dotenv

# allow the port
ufw allow 8000

# python manage.py runserver 0.0.0.0:8000


