import subprocess
import sys

from django.core.management.base import NoArgsCommand


class Command( NoArgsCommand ):

	help = 'only tests galtrace apps'

	def handle_noargs( self, **options ):
		a = subprocess.call( [ 'python', '-m', 'unittest', 'galtrace.libs.crawler.tests' ] )
		b = subprocess.call( [ 'python', 'manage.py', 'test', 'core' ] )
		if any( ( a, b ) ):
			sys.exit( 1 )
