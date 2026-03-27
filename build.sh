#!/usr/bin/env bash

pip install -r requirements.txt

echo "Making migrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static..."
python manage.py collectstatic --noinput