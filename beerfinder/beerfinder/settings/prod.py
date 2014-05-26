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

ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split()
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get('SMTP_HOST')
EMAIL_HOST_USER = os.environ.get('SMTP_USER')
EMAIL_HOST_PASSWORD = os.environ.get('SMTP_PASSWORD')
EMAIL_PORT = os.environ.get('SMTP_PORT', 587)
REGISTRATION_OPEN = True
