"""
Django settings for openshift
"""
import os
from openshift import libs
from %DJANGO_SETTINGS_MODULE% import *

DATA_DIR = os.path.dirname(os.environ.get('OPENSHIFT_DATA_DIR'))

DEBUG = True if ('true' == os.environ.get('DJANGO_DEBUG', 'false')) else False
TEMPLATE_DEBUG = DEBUG

if os.environ.has_key('OPENSHIFT_MYSQL_DB_HOST'):
    DATABASES = {
        'default': {
            'ENGINE' : 'django.db.backends.mysql',
            'NAME' : os.environ.get('OPENSHIFT_APP_NAME'),
            'USER' : os.environ.get('OPENSHIFT_MYSQL_DB_USERNAME'),
            'PASSWORD' : os.environ.get('OPENSHIFT_MYSQL_DB_PASSWORD'),
            'HOST' : os.environ.get('OPENSHIFT_MYSQL_DB_HOST'),
            'PORT' : os.environ.get('OPENSHIFT_MYSQL_DB_PORT'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(DATA_DIR, 'db.sqlite3'),
        }
    }

ALLOWED_HOSTS = [
    os.environ.get('OPENSHIFT_GEAR_DNS'),
]

# Generates secure key
uses_keys = libs.openshift_secure({ 'SECRET_KEY': SECRET_KEY })
SECRET_KEY = uses_keys['SECRET_KEY']

MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
STATIC_ROOT = os.path.join(DATA_DIR, 'static')

if 'gunicorn' not in INSTALLED_APPS:
    INSTALLED_APPS += ('gunicorn',)

try:
    if 'version' in LOGGING:
        pass
except NameError:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {},
        'handlers': {},
        'loggers': {},
    }

if 'formatters' not in LOGGING:
    LOGGING['formatters'] = {}

LOGGING['formatters']['gunicorn'] = {
    'format': '%(asctime)s [%(process)s] [%(levelname)s] %(name)s - %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S',
}

if 'handlers' not in LOGGING:
    LOGGING['handlers'] = {}

LOGGING['handlers']['gunicorn'] = {
    'level': 'DEBUG',
    'class': 'logging.StreamHandler',
    'formatter': 'gunicorn',
}

if 'loggers' not in LOGGING:
    LOGGING['loggers'] = {}

LOGGING['loggers'][''] = {
    'handlers': ['gunicorn'],
    'level': 'DEBUG' if DEBUG else 'INFO',
    'propagate': True,
}
