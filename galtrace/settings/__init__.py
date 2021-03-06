import base64
import json
import os
import subprocess


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
GALTRACE_SETTINGS_ROOT = os.path.join(BASE_DIR, 'galtrace/settings')
GALTRACE_HEROKU_CONFIG_KEY = 'GALTRACE_SECRET'


def fromLocalEnvironment():
    tmp = os.environ[GALTRACE_HEROKU_CONFIG_KEY]
    tmp = base64.b64decode(tmp)
    tmp = json.loads(tmp)
    return tmp

def fromRemoteEnvironment():
    tmp = subprocess.check_output(['heroku', 'config:get', GALTRACE_HEROKU_CONFIG_KEY])
    tmp = tmp.strip()
    tmp = base64.b64decode(tmp)
    tmp = json.loads(tmp)
    return tmp

def fromJsonFile():
    tmp = os.path.join(GALTRACE_SETTINGS_ROOT, 'secret.json')
    tmp = open(tmp, 'r')
    secret = json.load(tmp)
    tmp.close()
    return secret


TIME_ZONE = 'Asia/Taipei'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

WSGI_APPLICATION = 'galtrace.wsgi.application'

TEMPLATE_DIRS = (
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'galtrace.libs.core',
    'galtrace.apps.frontend',
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

# login settings
LOGIN_URL = '/'
