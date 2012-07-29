import private.settings

PRIVATE_SETTINGS = private.settings.load()

DEBUG = PRIVATE_SETTINGS['DEBUG']
TEMPLATE_DEBUG = DEBUG

ADMINS = PRIVATE_SETTINGS['ADMINS']

MANAGERS = ADMINS

DATABASES = PRIVATE_SETTINGS['DATABASES']

TIME_ZONE = 'Asia/Taipei'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = ''

MEDIA_URL = ''

STATIC_ROOT = PRIVATE_SETTINGS['STATIC_ROOT']

STATIC_URL = '/static/'

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = PRIVATE_SETTINGS['SECRET_KEY']

TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.gzip.GZipMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.transaction.TransactionMiddleware',
)

ROOT_URLCONF = 'galtrace.urls'

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
	'django.contrib.admin',

	'gunicorn',

	'kernel',
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

# email settings
EMAIL_HOST = PRIVATE_SETTINGS['EMAIL_HOST']
EMAIL_HOST_PASSWORD = PRIVATE_SETTINGS['EMAIL_HOST_PASSWORD']
EMAIL_HOST_USER = PRIVATE_SETTINGS['EMAIL_HOST_USER']
EMAIL_PORT = PRIVATE_SETTINGS['EMAIL_PORT']
EMAIL_USE_TLS = PRIVATE_SETTINGS['EMAIL_USE_TLS']
SERVER_EMAIL = PRIVATE_SETTINGS['SERVER_EMAIL']

# login settings
LOGIN_URL = '/'
