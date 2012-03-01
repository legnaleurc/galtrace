def load( *args, **kwargs ):
	import os, json
	if 'DATABASE_URL' in os.environ:
		return {
			'DATABASES': None,
			'SECRET_KEY': os.environ['SECRET_KEY'],
		}

	data = json.load( os.path.join( args[0], 'private/data.json' ) )
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
