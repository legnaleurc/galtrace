def load( *args, **kwargs ):
	import os, json
	if 'DATABASE_URL' in os.environ:
		return {
			'DATABASES': {
			},
			'SECRET_KEY': os.environ['SECRET_KEY'],
		}

	data = json.load( open( os.path.join( args[0], 'private/data.json' ), 'r' ) )
	return {
		'DATABASES': {
			'default': {
				'ENGINE': 'django.db.backends.sqlite3',
				'NAME': os.path.join( args[0], 'private/default.sqlite' ),
				'USER': '',
				'PASSWORD': '',
				'HOST': '',
				'PORT': '',
			}
		},
		'SECRET_KEY': data['SECRET_KEY'],
	}
