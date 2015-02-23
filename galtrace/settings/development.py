from os.path import join

from . import *


GALTRACE_DATABASE_PATH = join(GALTRACE_SETTINGS_ROOT, 'default.sqlite')
GALTRACE_SECRET = fromJsonFile()


DEBUG = True

TEMPLATE_DEBUG = DEBUG

ADMINS = GALTRACE_SECRET['ADMINS']

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': GALTRACE_DATABASE_PATH,
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    },
}

SECRET_KEY = GALTRACE_SECRET['SECRET_KEY']

ROOT_URLCONF = 'galtrace.urls.development'

INSTALLED_APPS += (
    'galtrace.libs.cmds',
)
