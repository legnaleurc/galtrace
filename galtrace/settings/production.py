import base64
import json
import os

import dj_database_url

from . import *


GALTRACE_SECRET = json.loads( base64.b64decode( os.environ[GALTRACE_HEROKU_CONFIG_KEY] ) )


DEBUG = False

TEMPLATE_DEBUG = DEBUG

ADMINS = GALTRACE_SECRET['ADMINS']

MANAGERS = ADMINS

DATABASES = {
	'default': dj_database_url.config(),
}

SECRET_KEY = GALTRACE_SECRET['SECRET_KEY']

MIDDLEWARE_CLASSES = (
	'beproud.django.ssl.middleware.SSLProxyMiddleware',
) + MIDDLEWARE_CLASSES + (
	'beproud.django.ssl.middleware.SSLRedirectMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS += (
	'beproud.django.ssl.context_processors.conf',
)

INSTALLED_APPS += (
	'beproud.django.ssl',
)

# email settings
EMAIL_BACKEND = 'galtrace.mail.GmailBackend'
EMAIL_HOST = GALTRACE_SECRET['EMAIL_HOST']
EMAIL_HOST_PASSWORD = GALTRACE_SECRET['EMAIL_HOST_PASSWORD']
EMAIL_HOST_USER = GALTRACE_SECRET['EMAIL_HOST_USER']
EMAIL_PORT = GALTRACE_SECRET['EMAIL_PORT']
EMAIL_USE_TLS = GALTRACE_SECRET['EMAIL_USE_TLS']
GOOGLE_API_CLIENT_ID = GALTRACE_SECRET['GOOGLE_API_CLIENT_ID']
GOOGLE_API_CLIENT_SECRET = GALTRACE_SECRET['GOOGLE_API_CLIENT_SECRET']
SERVER_EMAIL = GALTRACE_SECRET['SERVER_EMAIL']

# ssl settings
SECURE_PROXY_SSL_HEADER = ( 'HTTP_X_FORWARDED_PROTO', 'https' )
SSL_URLS = (
	r'^.*$',
)
