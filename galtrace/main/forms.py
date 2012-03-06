from django import forms

from main.models import Order, PHASES

import json

class RestoreForm( forms.Form ):
	data = forms.FileField()

	def save( self, user ):
		data_ = self.cleaned_data['data']
		data_ = json.load( data_ )
		rows = data_['orders']
		Order.objects.all().delete()
		for row in rows:
			o = Order( user = user, **row )
			o.save()

		# NOTE for PostgreSQL, it must update next pk by hand
		import os
		if 'DATABASE_URL' in os.environ:
			from django.db import connection, transaction
			query = connection.cursor()
			query.execute( 'SELECT setval(pg_get_serial_sequence(\'"main_order"\',\'id\'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "main_order";' )
			transaction.commit_unless_managed()

		return True

class OrderForm( forms.ModelForm ):
	class Meta:
		model = Order
		fields = ( 'uri', 'title', 'vendor', 'date', 'phase' )
		widgets = {
			'phase': forms.Select( choices = PHASES ),
		}
