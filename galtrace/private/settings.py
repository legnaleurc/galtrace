import os, json

PRIVATE_DIR = os.path.dirname( os.path.abspath( __file__ ) )

def load( *args, **kwargs ):
	if 'DATABASE_URL' in os.environ:
		private = {
			'DATABASES': {
			},
			'DEBUG': False,
		}
		data = json.loads( os.environ['PRIVATE_DATA'] )
	else:
		private = {
			'DATABASES': {
				'default': {
					'ENGINE': 'django.db.backends.sqlite3',
					'NAME': os.path.join( PRIVATE_DIR, 'default.sqlite' ),
					'USER': '',
					'PASSWORD': '',
					'HOST': '',
					'PORT': '',
				}
			},
			'DEBUG': True,
		}
		data = json.load( open( os.path.join( PRIVATE_DIR, 'data.json' ), 'r' ) )

	private.update( {
		'EMAIL_HOST': data['EMAIL_HOST'],
		'EMAIL_HOST_PASSWORD': data['EMAIL_HOST_PASSWORD'],
		'EMAIL_HOST_USER': data['EMAIL_HOST_USER'],
		'EMAIL_PORT': data['EMAIL_PORT'],
		'EMAIL_USE_TLS': data['EMAIL_USE_TLS'],
		'SECRET_KEY': data['SECRET_KEY'],
		'SERVER_EMAIL': data['SERVER_EMAIL'],
	} )

	private['ADMINS'] = tuple( ( t[0], t[1] ) for t in data['ADMINS'] )

	return private

if __name__ == '__main__':
	import subprocess, sys
	data = json.load( open( os.path.join( PRIVATE_DIR, 'data.json' ), 'r' ) )
	ret = subprocess.call( [ 'heroku', 'config:add', 'PRIVATE_DATA={0}'.format( json.dumps( data, separators = ( ',', ':' ) ) ) ] )
	sys.exit( ret )
