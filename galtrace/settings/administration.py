from os.path import join
import subprocess

import dj_database_url

from . import *


def getDBURL():
    url = subprocess.check_output(['heroku', 'config:get', 'DATABASE_URL'])
    return url.strip()

GALTRACE_SECRET = fromRemoteEnvironment()


DEBUG = True

TEMPLATE_DEBUG = DEBUG

ADMINS = GALTRACE_SECRET['ADMINS']

MANAGERS = ADMINS

DATABASES = {
    'default': dj_database_url.parse(getDBURL()),
}

SECRET_KEY = GALTRACE_SECRET['SECRET_KEY']

ROOT_URLCONF = 'galtrace.urls.administration'

INSTALLED_APPS += (
    'django.contrib.admin',
    'galtrace.apps.backend',
)
