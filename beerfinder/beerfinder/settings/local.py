from .base import *

TEMPLATE_DEBUG = DEBUG = True
CELERY_DEFAULT_QUEUE = 'beerfinder_dev'
CELERY_ALWAYS_EAGER = True
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}
