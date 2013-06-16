import hashlib
import os

from django.db import models
from django.contrib.auth.models import User

PHASES = ( ( 0, u'todo' ), ( 1, u'get' ), ( 2, u'opened' ), ( 3, u'half' ), ( 4, u'finished' ) )

class OrderManager( models.Manager ):
	def dump( self, user ):
		rows = super( OrderManager, self ).filter( user__exact = user )
		orders = []
		for row in rows:
			orders.append( {
				'title': row.title,
				'vendor': row.vendor,
				'date': row.date,
				'uri': row.uri,
				'phase': row.phase,
				'volume': row.volume,
			} )
		data = {
			'version': 1,
			'orders': orders,
		}
		return data

	def restore( self, user, data ):
		if data['version'] != 1:
			return False
		rows = data['orders']
		super( OrderManager, self ).filter( user__exact = user ).delete()
		for row in rows:
			args = dict( ( x, row[x] ) for x in ( 'title', 'vendor', 'date', 'uri', 'phase', 'volume' ) )
			# FIXME dangerous, please check data
			o = Order( user = user, **args )
			o.save()
		return True

def getImageName( instance, filename ):
	name, ext = os.path.splitext( filename )
	name = hashlib.sha1( instance.title.encode( 'utf-8' ) ).hexdigest()
	return u'{0}/{1}{2}'.format( instance.user.username, name, ext )

class Order( models.Model ):
	objects = OrderManager()

	user = models.ForeignKey( User )
	title = models.CharField( max_length = 255 )
	vendor = models.CharField( max_length = 255 )
	date = models.CharField( max_length = 15 )
	uri = models.CharField( max_length = 65535 )
	thumb = models.ImageField( upload_to = getImageName, max_length = 65535, null = True )
	phase = models.IntegerField()
	volume = models.IntegerField()
