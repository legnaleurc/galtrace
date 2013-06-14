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
			# FIXME dangerous, please check data
			o = Order( user = user, **row )
			o.save()
		return True

class Order( models.Model ):
	objects = OrderManager()

	user = models.ForeignKey( User )
	title = models.CharField( max_length = 255 )
	vendor = models.CharField( max_length = 255 )
	date = models.CharField( max_length = 15 )
	uri = models.CharField( max_length = 65535 )
	phase = models.IntegerField()
	volume = models.IntegerField()
