"""
Django settings for purge_proy project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import djcelery
from kombu import Queue, Exchange
# _dir = os.pathdirname(__file__)
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bb5jg0v(e82k!f7ls_7e$2lx9$#)13mjby_$8(hphcno^21v--'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']
ADMIN_SITE_NAME = 'My Admin Site'
ADMIN_SITE_DESCRIPTION = 'This is a private site.  Please don\'t hack me'

TASK_PURGE = True

# Application definition

INSTALLED_APPS = [
    #    'purge.apps.PurgesConfig',
    'purge',
    'bootstrap3',
    'djcelery',
    'kombu.transport.django',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'purge_proy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'purge_proy.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vacapur',
        'USER': 'devo',
        'PASSWORD': 'devo_pass',
        'HOST': 'localhost',
        'PORT': '',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

# Celery
# CELERY_TIMEZONE = TIME_ZONE
CELERY_ACCEPT_CONTENT = ['json', 'pickle']
CELERYD_CONCURRENCY = 2
CELERYD_MAX_TASKS_PER_CHILD = 4
CELERYD_PREFETCH_MULTIPLIER = 1
CELERY_TASK_SERIALIZER = 'json'

CELERY_DEFAULT_QUEUE = 'purge'
CELERY_DEFAULT_EXCHANGE_TYPE = 'purge_e'
CELERY_DEFAULT_ROUTING_KEY = 'purge_r'
CELERY_QUEUES = (
    Queue('purge', Exchange('default'), routing_key='purge_r'),
)
# python manage.py celery worker -Q purge -n purge_worker


CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
# BROKER_URL = 'amqp://purge:purge_pass@127.0.0.1:5672//' # para usar Rabbitmq
BROKER_URL = 'django://'    # Usa BD de Django
djcelery.setup_loader()

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Chile/Continental'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
# print(STATIC_ROOT)
