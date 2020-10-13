# noinspection PyUnresolvedReferences
from collab_coursebook.settings import *

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']

SECRET_KEY = 'SECRET'

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'HOST': '127.0.0.1',
#         'NAME': 'test',
#         'USER': 'django',
#         'PASSWORD': 'test'
#     }
# }