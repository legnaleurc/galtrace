import os, json

PRIVATE_DIR = os.path.dirname( os.path.abspath( __file__ ) )
PRIVATE_KEY = 'GALTRACE_DATA'
PRIVATE_DATA_PATH = os.path.join( PRIVATE_DIR, 'data.json' )
PRIVATE_DATABASE_PATH = os.path.join( PRIVATE_DIR, 'default.sqlite' )

def load( *args, **kwargs ):
	if PRIVATE_KEY in os.environ:
		data = json.loads( os.environ[PRIVATE_KEY] )
		import dj_database_url
		private = {
			'ADMIN_MEDIA_PREFIX': data['ADMIN_MEDIA_PREFIX'],
			'DATABASES': {
				'default': dj_database_url.config(),
			},
			'DEBUG': False,
			'STATIC_URL': data['STATIC_URL'],
		}
	else:
		private = {
			'ADMIN_MEDIA_PREFIX': '/static/admin/',
			'DATABASES': {
				'default': {
					'ENGINE': 'django.db.backends.sqlite3',
					'NAME': PRIVATE_DATABASE_PATH,
					'USER': '',
					'PASSWORD': '',
					'HOST': '',
					'PORT': '',
				},
			},
			'DEBUG': True,
			'STATIC_URL': '/static/',
		}
		data = json.load( open( PRIVATE_DATA_PATH, 'r' ) )

	private.update( {
		'ADMINS': ( ( t[0], t[1] ) for t in data['ADMINS'] ),
		'EMAIL_HOST': data['EMAIL_HOST'],
		'EMAIL_HOST_PASSWORD': data['EMAIL_HOST_PASSWORD'],
		'EMAIL_HOST_USER': data['EMAIL_HOST_USER'],
		'EMAIL_PORT': data['EMAIL_PORT'],
		'EMAIL_USE_TLS': data['EMAIL_USE_TLS'],
		'SECRET_KEY': data['SECRET_KEY'],
		'SERVER_EMAIL': data['SERVER_EMAIL'],
		'STATIC_ROOT': os.path.join( PRIVATE_DIR, '../static/' ),
	} )

	return private

if __name__ == '__main__':
	import subprocess, sys
	data = json.load( open( PRIVATE_DATA_PATH, 'r' ) )
	ret = subprocess.call( [ 'heroku', 'config:add', '{0}={1}'.format( PRIVATE_KEY, json.dumps( data, separators = ( ',', ':' ) ) ) ] )
	sys.exit( ret )
