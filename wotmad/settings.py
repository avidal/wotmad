from path import path

PROJECT_ROOT = path(__file__).abspath().dirname()
SITE_ROOT = PROJECT_ROOT.dirname()
SITE_URL = 'http://chrono.local:8000'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Alex Vidal', 'alex.vidal@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': SITE_ROOT / 'tmp' / 'database.db',
    }
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
    'compressor.finders.CompressorFinder',
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

    'compressor',
    'django_browserid',
)

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
            '()': 'django.utils.log.RequireDebugFalse'
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

COMPRESS_OUTPUT_DIR = '_cache'

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

BROWSERID_CREATE_USER = True
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/?login=true'
LOGIN_REDIRECT_URL_FAILURE = '/?login=failure'
