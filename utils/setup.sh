#!/usr/bin/env bash
# Setup Collab Coursebook
# execute as utils/setup.sh

# abort on error, print executed commands
set -ex

# remove old virtualenv
rm -rf venv/

# Setup Python Environment
# Requires: Virtualenv, appropriate Python installation
virtualenv venv -p python3
source venv/bin/activate
pip install --upgrade setuptools pip wheel
pip install -r requirements.txt

# Install poppler (for pdf2image)
sudo apt-get install -y poppler-utils libmagic1 gettext

# Setup database
python manage.py migrate
python manage.py createinitialrevisions

# Prepare static files and translations
python manage.py collectstatic --noinput
python manage.py compilemessages --ignore=cache --ignore=venv

# Create superuser
# Credentials are entered interactively on CLI
python manage.py createsuperuser

deactivate
