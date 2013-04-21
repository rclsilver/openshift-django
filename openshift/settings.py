"""
Django settings for openshift
"""
import os
from unipath import FSPath as Path
from openshift import libs
from %DJANGO_SETTINGS_MODULE% import *

DATA_DIR = Path(os.environ.get('OPENSHIFT_DATA_DIR'))
LOG_DIR = Path(os.environ.get('OPENSHIFT_DIY_LOG_DIR'))

DEBUG = True if ('true' == os.environ.get('DJANGO_DEBUG', 'false')) else False
TEMPLATE_DEBUG = DEBUG

if os.environ.has_key('OPENSHIFT_MYSQL_DB_HOST'):
    DATABASES = {
        'default': {
            'ENGINE' : 'django.db.backends.mysql',
            'NAME' : os.environ['OPENSHIFT_APP_NAME'],
            'USER' : os.environ['OPENSHIFT_MYSQL_DB_USERNAME'],
            'PASSWORD' : os.environ['OPENSHIFT_MYSQL_DB_PASSWORD'],
            'HOST' : os.environ['OPENSHIFT_MYSQL_DB_HOST'],
            'PORT' : os.environ['OPENSHIFT_MYSQL_DB_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': DATA_DIR.child('library.db'),
        }
    }

ALLOWED_HOSTS = [
    os.environ['OPENSHIFT_GEAR_DNS'],
]

# Generates secure key
uses_keys = libs.openshift_secure({ 'SECRET_KEY': SECRET_KEY })
SECRET_KEY = uses_keys['SECRET_KEY']

if 'handlers' in LOGGING and 'logfile' in LOGGING['handlers']:
    LOGGING['handlers']['logfile']['filename'] = LOG_DIR.child('%s.log' % os.environ.get('OPENSHIFT_APP_NAME'))

if MEDIA_ROOT != '':
    MEDIA_ROOT = DATA_DIR.child('media')

if 'gunicorn' not in INSTALLED_APPS:
    INSTALLED_APPS += ('gunicorn',)

