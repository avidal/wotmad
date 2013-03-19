import os

from path import path

PROJECT_ROOT = path(__file__).abspath().dirname()
SITE_ROOT = PROJECT_ROOT.dirname()
ENV = os.environ.get('ENV', 'dev')

SITE_URL_MAP = {
    'heroku': 'http://wotmad.herokuapp.com',
    'dev': 'http://wotmad.local:5000',
}

# First, try loading SITE_URL out of the environment
# If that fails, load it out of the map
SITE_URL = os.environ.get('SITE_URL', None)

if not SITE_URL:
    SITE_URL = SITE_URL_MAP.get(ENV, None)

if not SITE_URL:
    from django.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured("No SITE_URL specified.")

if ENV == 'dev':
    DEBUG = True
elif ENV == 'heroku':
    DEBUG = False
else:
    DEBUG = False

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Alex Vidal', 'alex.vidal@gmail.com'),
)

MANAGERS = ADMINS

INTERNAL_IPS = ('127.0.0.1',)

import dj_database_url

DEFAULT_DATABASE = 'sqlite:////' + (SITE_ROOT / 'tmp' / 'database.db')
DATABASES = {'default': dj_database_url.config(default=DEFAULT_DATABASE)}

if 'postgres' in DATABASES['default']['ENGINE']:
    DATABASES['default']['ENGINE'] = 'django_postgrespool'
    SOUTH_DATABASE_ADAPTERS = {
        'default': 'south.db.postgresql_psycopg2'
    }

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = SITE_ROOT / 'uploads'

MEDIA_URL = '/uploads/'

STATIC_ROOT = SITE_ROOT / 'static'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    PROJECT_ROOT / 'assets',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '0uni4qeb$0hu*y#iap93)%!(_lr2syps+8p+3-sybk9k%e^vy&amp;'

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
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

if DEBUG:
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

ROOT_URLCONF = 'wotmad.urls'

WSGI_APPLICATION = 'wotmad.wsgi.application'

TEMPLATE_DIRS = (
    PROJECT_ROOT / 'templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'django_browserid',
    'crispy_forms',
    'south',

    'wotmad.accounts',
    'wotmad.artofwar',
    'wotmad.scripts',
    'wotmad.stats',
)

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'wotmad.backends.BrowserIDBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django_browserid.context_processors.browserid_form",
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
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

BROWSERID_CREATE_USER = True
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'
LOGIN_REDIRECT_URL = '/accounts/login/redirect/'
LOGIN_REDIRECT_URL_FAILURE = '/accounts/login/failure/'

CRISPY_FAIL_SILENTLY = not DEBUG
