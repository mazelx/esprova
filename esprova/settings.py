"""
Django settings for esprova project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from urllib.parse import urlparse

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False)

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['esprova.herokuapp.com', '.esprova.com', 'esprova-staging.herokuapp.com']


# Application definition

INSTALLED_APPS = (
    # admin should be first (need to list applications)
    'django.contrib.admin',


    # project applications
    'core',
    'search_backends',
    'planning',
    'accounts',
    'registration',

    # External modules
    # 'debug_toolbar',

    'django_countries',
    'haystack',
    'rest_framework',
    'django_nose',
    'django_extensions',
    'storages',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.formtools',
    'django.contrib.humanize',
    # optional but advised for registration app
    'django.contrib.sites',

)

MIDDLEWARE_CLASSES = (
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',

)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    #  Gestion de l'i18n
    "django.core.context_processors.i18n",

    'core.context_processors.global_settings',
)

ROOT_URLCONF = 'esprova.urls'

WSGI_APPLICATION = 'esprova.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# Django settings.py

import dj_database_url
DATABASES = {
             'default': dj_database_url.config()
             }


redis_url = urlparse(os.environ.get('REDISCLOUD_URL'))
CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': '%s:%s' % (redis_url.hostname, redis_url.port),
            'OPTIONS': {
                'PASSWORD': redis_url.password,
                'DB': 0,
            }
        }
    }

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# LOGIN_URL = "/login"
# LOGIN_REDIRECT_URL = "/"

 # ------ Project Specific Settings ------

GOOGLE_API_KEY = "AIzaSyAu5lWzzuB7WXLqI9UzK2yL0IVtyr97yOg"



bonsai_url = os.environ.get('BONSAI_URL')

# Haystack -----------
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'search_backends.elastic_backend.CustomElasticSearchEngine',
        'URL': bonsai_url,
        'INDEX_NAME': 'haystack',
    },
}

# HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_SIGNAL_PROCESSOR = 'core.signals.RaceOnlySignalProcessor'

# Haystack -----------
ELASTICSEARCH_INDEX_SETTINGS = {
    'settings': {
        "number_of_shards": 9,
        "analysis": {
            "analyzer": {
                "search_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "asciifolding"]
                },
                "ngram_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["haystack_ngram"]
                },
                "edgengram_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["haystack_edgengram", "lowercase", "asciifolding"],
                }
            },
            "tokenizer": {
                "haystack_ngram_tokenizer": {
                    "type": "nGram",
                    "min_gram": 3,
                    "max_gram": 15,
                },
                "haystack_edgengram_tokenizer": {
                    "type": "edgeNGram",
                    "min_gram": 2,
                    "max_gram": 15,
                    "side": "front"
                }
            },
            "filter": {
                "frsnowball": {
                    "type": "snowball",
                    "language": "French"
                },
                "haystack_ngram": {
                    "type": "nGram",
                    "min_gram": 3,
                    "max_gram": 15,
                    "token_chars": [
                        "letter",
                        "digit",
                        "punctuation",
                        "symbol"
                    ]
                },
                "haystack_edgengram": {
                    "type": "edgeNGram",
                    "min_gram": 2,
                    "max_gram": 15
                }
            }
        }
    }
}


# Nose -----------
# Use nose to run all tests
# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Tell nose to measure coverage on the 'foo' and 'bar' apps
NOSE_ARGS = [
    # '--with-coverage',
    # '--cover-package=core.views, core.models, api.serializers, api.views',
]


# Django Static
# Where to find the static files ?
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

STATIC_ROOT = os.path.join(BASE_DIR, "static_out")

# AWS -----------

# Amazon Web Services header, see http://developer.yahoo.com/performance/rules.html#expires
AWS_HEADERS = {
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'Cache-Control': 'max-age=94608000',
}

AWS_STORAGE_BUCKET_NAME = 'esprova-static'
AWS_ACCESS_KEY_ID = 'AKIAIBSDSZFEOYKIWZTA'
AWS_SECRET_ACCESS_KEY = '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'

# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
# you run `collectstatic`).
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# This is used by the `static` template tag from `static`, if you're using that. Or if anything else
# refers directly to STATIC_URL. So it's safest to always set it.
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN


# Django REST Framework
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )

}

SITE_ID = 1


# REGISTRATION
ACCOUNT_ACTIVATION_DAYS = 7


# EMAIL SETTING
EMAIL_HOST = 'mail.privateemail.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'contact@esprova.com'
EMAIL_HOST_PASSWORD = '.GNS25eiu.'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'contact@esprova.com'


# Development settings :
# local_settings.py only exists on dev hosts and contains dev specific settings
try:
    from esprova.local_settings import *
except ImportError as e:
    pass
