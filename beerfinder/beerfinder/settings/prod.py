from .base import *

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
