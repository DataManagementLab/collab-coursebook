#!/usr/bin/env bash
# Regular maintenance tasks for Collab Coursebook
# execute as utils/cron.sh

# abort on error, print executed commands
set -ex

# activate virtualenv if necessary
if [ -z ${VIRTUAL_ENV+x} ]; then
    source venv/bin/activate
fi

# set environment variable when we want to update in production
if [ "$1" = "--prod" ]; then
    export DJANGO_SETTINGS_MODULE=collab_coursebook.settings_production
fi

./manage.py clearsessions
./manage.py django_cas_ng_clean_sessions
