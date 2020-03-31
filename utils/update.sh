#!/usr/bin/env bash
# Update Collab Coursebook
# execute as utils/update.sh

# abort on error, print executed commands
set -ex

# activate virtualenv if necessary
if [ -z ${VIRTUAL_ENV+x} ]; then
    source venv/bin/activate
fi

# set environment variable when we want to update in production
if [ "$1" = "--prod" ]; then
    export DJANGO_SETTINGS_MODULE=AKPlanning.settings_production
fi

git pull
pip install --upgrade setuptools pip wheel
pip install --upgrade -r requirements.txt

./manage.py migrate
./manage.py collectstatic --noinput
./manage.py compilemessages

touch collab_coursebook/wsgi.py
