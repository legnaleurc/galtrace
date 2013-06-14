import base64
import json
import subprocess

from django.conf import settings
from django.core.management.base import NoArgsCommand


class Command( NoArgsCommand ):

	help = 'pushs local secret to remote environment'

	def handle_noargs( self, **options ):
		secret = json.dumps( settings.GALTRACE_SECRET, separators = ( ',', ':' ) )
		secret = base64.b64encode( secret )
		ret = subprocess.call( [ 'heroku', 'config:set', '{0}={1}'.format( settings.GALTRACE_HEROKU_CONFIG_KEY, secret ) ] )
