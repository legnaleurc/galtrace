import dj_database_url

from . import *


GALTRACE_SECRET = fromLocalEnvironment()


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

ROOT_URLCONF = 'galtrace.urls.production'

INSTALLED_APPS += (
	'beproud.django.ssl',
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
	'galtrace.herokuapp.com',
]
SECURE_PROXY_SSL_HEADER = ( 'HTTP_X_FORWARDED_PROTO', 'https' )
SSL_URLS = (
	r'^.*$',
)
