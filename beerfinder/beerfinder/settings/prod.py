from .base import *
import os

TEMPLATE_DEBUG = DEBUG = False
CELERY_DEFAULT_QUEUE = 'beerfinder'
CELERY_ALWAYS_EAGER = False
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
        'OPTIONS': {
            'DB': 1,
            },
        },
    }

ALLOWED_HOSTS = ['beer.bash-shell.net']
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('SMTP_HOST')
EMAIL_HOST_USER = os.environ.get('SMTP_USER')
EMAIL_HOST_PASSWORD = os.environ.get('SMTP_PASSWORD')
EMAIL_PORT = os.environ.get('SMTP_PORT')
EMAIL_USE_SSL = True
EMAIL_USE_TLS = True
DEBUG = True
