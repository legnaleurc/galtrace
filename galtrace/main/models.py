from django.db import models
from django.contrib.auth.models import User

PHASES = [ ( 0, 'Todo' ), ( 1, 'Get' ), ( 2, 'Opened' ), ( 3, 'Half' ), ( 4, 'Finished' ) ]

class Order( models.Model ):
	user = models.ForeignKey( User )
	title = models.CharField( max_length = 255 )
	vendor = models.CharField( max_length = 255 )
	date = models.CharField( max_length = 15 )
	uri = models.CharField( max_length = 65535 )
	phase = models.IntegerField()
	volume = models.IntegerField()
