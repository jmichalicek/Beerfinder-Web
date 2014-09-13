"""
Django settings for beerfinder project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url

try:
    from .git_head import *
except ImportError:
    # could make this a modified time on a file?
    REQUIRE_BUILD_PATH = ''

SITE_ID = 1;

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

AUTH_USER_MODEL = 'accounts.User'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'aw7&p1479lum9@0%=)4ges7_f4k6p+--tlp%eh0)x73u-2bsn#')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.gis',
    # 3rd party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'djcelery',
    'django_extensions',
    'widget_tweaks',
    'require',
    # my apps
    'accounts',
    'beer',
    'sighting',
    'venue',
    'watchlist'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
                               "django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.media",
                               "django.core.context_processors.static",
                               "django.core.context_processors.tz",
                               "django.contrib.messages.context_processors.messages",
                               "django.core.context_processors.request",
                               # allauth specific context processors
                               "allauth.account.context_processors.account",
                               "allauth.socialaccount.context_processors.socialaccount",
                               "core.context_processors.site_processor")

ROOT_URLCONF = 'beerfinder.urls'

WSGI_APPLICATION = 'beerfinder.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
ADMINS = (
    ('Justin Michalicek', 'jmichalicek@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {'default': dj_database_url.config(
        #engine='django.contrib.gis.db.backend.spatialite',
        default='sqlite:////{0}'.format(os.path.join(BASE_DIR, 'beerfinder.sqlite'))),
}
#DATABASES = {'default': dj_database_url.config()}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/%s/' % REQUIRE_BUILD_PATH
STATIC_ROOT = os.path.join(BASE_DIR, 'static', REQUIRE_BUILD_PATH)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
)

AUTHENTICATION_BACKENDS = (
     # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
 )

LOGIN_REDIRECT_URL = 'sightings_list'

FOURSQUARE_CLIENT_ID = os.environ.get('FOURSQUARE_CLIENT_ID')
FOURSQUARE_CLIENT_SECRET = os.environ.get('FOURSQUARE_CLIENT_SECRET')

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ACCOUNT_ADAPTER = 'accounts.adapters.RegistrationTogglableAdapter'
REGISTRATION_OPEN = False

# celery stuff
#BROKER_URL = 'redis://localhost:6379/0'
CELERYD_HIJACK_ROOT_LOGGER = False
BROKER_URL = 'redis://'
CELERY_RESULT_BACKEND = 'redis://'
BROKER_TRANSPORT_OPTIONS = {'fanout_prefix': True}

TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY')
TWITTER_API_SECRET = os.environ.get('TWITTER_API_SECRET')

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

IMAGEKIT_DEFAULT_CACHEFILE_BACKEND = 'imagekit.cachefiles.backends.Celery'

REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 5
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
ACCOUNT_SESSION_REMEMBER = True


# django-require stuff
STATICFILES_STORAGE = 'require.storage.OptimizedStaticFilesStorage'
REQUIRE_BASE_URL = "js"

# The name of a build profile to use for your project, relative to REQUIRE_BASE_URL.
# A sensible value would be 'app.build.js'. Leave blank to use the built-in default build profile.
# Set to False to disable running the default profile (e.g. if only using it to build Standalone
# Modules)
REQUIRE_BUILD_PROFILE = 'app.build.js'

# The name of the require.js script used by your project, relative to REQUIRE_BASE_URL.
REQUIRE_JS = "vendor/require.js"

# A dictionary of standalone modules to build with almond.js.
# See the section on Standalone Modules, below.
#REQUIRE_STANDALONE_MODULES = {}
REQUIRE_DEBUG = DEBUG
REQUIRE_ENVIRONMENT = "core.require_environments.DebianNodeEnvironment"

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', '')
