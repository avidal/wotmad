import os

from path import path

from django.core.exceptions import ImproperlyConfigured

PROJECT_ROOT = path(__file__).abspath().dirname()
SITE_ROOT = PROJECT_ROOT.dirname()

# Use honcho to read the .env file, if it exists
if (SITE_ROOT / '.env').exists():
    from honcho.command import Honcho
    h = Honcho()
    entries = h.read_env(type('obj', (object,),
                              {'env': '.env', 'app_root': SITE_ROOT}))
    h.set_env(entries)
    del entries

DEFAULT_ENV = object()


def env(key, default=DEFAULT_ENV):
    v = os.environ.get(key, default)

    # If they tried to read a value that doesn't exist, and didn't provide
    # a default, then raise ImproperlyConfigured
    if v == DEFAULT_ENV:
        msg = "Environment variable '{0}' was not found.".format(key)
        raise ImproperlyConfigured(msg)

    if v == "True":
        v = True
    elif v == "False":
        v = False

    return v


SITE_URL = env('SITE_URL')
DEBUG = env('DEBUG', False)

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Alex Vidal', 'alex.vidal@gmail.com'),
)

MANAGERS = ADMINS

INTERNAL_IPS = ('127.0.0.1',)

import dj_database_url

DATABASE_URL = env('DATABASE_URL')
DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}

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
    'django_browserid.auth.BrowserIDBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
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
