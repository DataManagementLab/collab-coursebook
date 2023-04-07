#!/usr/bin/env bash
# run unit tests
# execute as Utils/test.sh

# activate virtualenv when necessary
if [ -z ${VIRTUAL_ENV+x} ]; then
    source venv/bin/activate
fi

# enable really all warnings, some of them are silenced by default
if [[ "$@" == *"--all"* ]]; then
    export PYTHONWARNINGS=all
fi

./manage.py test
./manage.py makemessages -l de_DE --ignore venv
python utils/check_translations.py
