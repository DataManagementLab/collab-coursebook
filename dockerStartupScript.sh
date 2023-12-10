#!/bin/sh
# Setup database
python manage.py migrate
python manage.py createinitialrevisions

# Prepare static files and translations
python manage.py collectstatic --noinput
python manage.py compilemessages --ignore=cache --ignore=venv

# Create superuser
# Credentials are entered interactively on CLI
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
