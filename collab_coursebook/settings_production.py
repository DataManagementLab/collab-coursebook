"""
This is the settings file used in production.
First, it imports all default settings, then overrides respective ones.
Secrets are stored in and imported from an additional file, not set under version control.
"""

import collab_coursebook.settings_secrets as secrets

# noinspection PyUnresolvedReferences
# from collab_coursebook.settings import *

### SECURITY ###

DEBUG = False

ALLOWED_HOSTS = secrets.HOSTS

SECRET_KEY = secrets.SECRET_KEY

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

### DATABASE ###

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'NAME': secrets.DB_NAME,
        'USER': secrets.DB_USER,
        'PASSWORD': secrets.DB_PASSWORD,
    }
}

# TODO: caching
