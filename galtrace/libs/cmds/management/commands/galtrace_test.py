import subprocess

from django.core.management.base import NoArgsCommand

class Command( NoArgsCommand ):

	help = 'only tests galtrace apps'

	def handle_noargs( self, **options ):
		subprocess.call( [ 'python', '-m', 'unittest', 'galtrace.libs.crawler.tests' ] )
		subprocess.call( [ 'python', 'manage.py', 'test', 'shell' ] )
