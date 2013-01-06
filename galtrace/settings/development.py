import base64
import json
from os.path import join
import subprocess
import sys

from . import *


GALTRACE_DATABASE_PATH = join( GALTRACE_SETTINGS_ROOT, 'default.sqlite' )
GALTRACE_SECRET_PATH = join( GALTRACE_SETTINGS_ROOT, 'secret.json' )
GALTRACE_SECRET = json.load( open( GALTRACE_SECRET_PATH, 'r' ) )


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
	},
}

SECRET_KEY = GALTRACE_SECRET['SECRET_KEY']


if __name__ == '__main__':
	secret = json.dumps( GALTRACE_SECRET, separators = ( ',', ':' ) )
	secret = base64.b64encode( secret )
	ret = subprocess.call( [ 'heroku', 'config:set', '{0}={1}'.format( GALTRACE_HEROKU_CONFIG_KEY, secret ) ] )
	sys.exit( ret )
