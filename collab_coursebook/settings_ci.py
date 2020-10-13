# noinspection PyUnresolvedReferences
from collab_coursebook.settings import *

DEBUG = False
SECRET_KEY = 'SECRET'

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