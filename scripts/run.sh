#!/bin/sh
# this will be used in root dockerfile 

set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate

uwsgi --socket :9000 --workers 4 --master --enable-threads --module pinmage.wsgi