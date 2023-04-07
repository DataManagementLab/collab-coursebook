#!/usr/bin/env bash
# Check the Collab Coursebook setup for potential problems
# execute as utils/check.sh

# activate virtualenv when necessary
if [ -z ${VIRTUAL_ENV+x} ]; then
    source venv/bin/activate
fi

# enable really all warnings, some of them are silenced by default
if [[ "$@" == *"--all"* ]]; then
    export PYTHONWARNINGS=all
fi

# in case of checking production setup
if [[ "$@" == *"--prod"* ]]; then
    export DJANGO_SETTINGS_MODULE=AKPlanning.settings_production
    ./manage.py check --deploy
fi

./manage.py check
./manage.py makemigrations --check
