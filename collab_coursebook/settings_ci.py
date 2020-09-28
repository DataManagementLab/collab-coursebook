from collab_coursebook.settings import *
import collab_coursebook.settings_secrets as secrets

DEBUG = False
SECRET_KEY = secrets.SECRET_KEY

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'NAME': 'test',
        'USER': 'django',
        'PASSWORD': 'test'
    }
}