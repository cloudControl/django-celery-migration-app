# Django settings for minestrone project.

import os
import json
import djcelery

from urlparse import urlparse

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1

with open(os.environ['CRED_FILE']) as cred_file:
    creds = json.load(cred_file)

mysqld_uri = urlparse(creds['MYSQLD']['MYSQLD_URL'])
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': mysqld_uri.path[1:],
        'USER': mysqld_uri.username,
        'PASSWORD': mysqld_uri.password,
        'HOST': mysqld_uri.hostname,
        'PORT': mysqld_uri.port
    }
}

djcelery.setup_loader()

BROKER_URL = creds['CLOUDAMQP']['CLOUDAMQP_URL']

# A very simple queue, just to illustrate the principle of routing.
CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = {
    'default': {
        'exchange': 'default',
        'exchange_type': 'topic',
        'binding_key': 'tasks.#'
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = '7bbxv&^4%f^en*c_c9*y+jrlfp+lwym$4b6((ok4v&8h9g%rwx'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'minestrone.urls'

WSGI_APPLICATION = 'minestrone.wsgi.application'

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
STATIC_ROOT = './static/'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'minestrone.soup',
    'djcelery',
    'gunicorn',
)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
