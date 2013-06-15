from os.path import join

from . import *


GALTRACE_DATABASE_PATH = join( GALTRACE_SETTINGS_ROOT, 'default.sqlite' )
GALTRACE_SECRET = fromJsonFile()


DEBUG = False

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
	},
}

SECRET_KEY = GALTRACE_SECRET['SECRET_KEY']

ROOT_URLCONF = 'galtrace.urls.vps'

STATICFILES_FINDERS += (
	'less.finders.LessFinder',
)

INSTALLED_APPS += (
	'less',
)

# email settings
EMAIL_BACKEND = 'galtrace.libs.mail.GmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = GALTRACE_SECRET['EMAIL_HOST_PASSWORD']
EMAIL_HOST_USER = GALTRACE_SECRET['EMAIL_HOST_USER']
EMAIL_PORT = 587
EMAIL_USE_TLS = True
GOOGLE_API_CLIENT_ID = GALTRACE_SECRET['GOOGLE_API_CLIENT_ID']
GOOGLE_API_CLIENT_SECRET = GALTRACE_SECRET['GOOGLE_API_CLIENT_SECRET']
SERVER_EMAIL = GALTRACE_SECRET['SERVER_EMAIL']

# ssl settings
ALLOWED_HOSTS = [
	'galtrace.wcpan.info',
]

# static files settings
STATIC_ROOT = GALTRACE_SECRET['STATIC_ROOT']
STATIC_URL = GALTRACE_SECRET['STATIC_URL']
