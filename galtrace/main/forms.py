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
			row['user'] = user
			o = Order( **row )
			o.save()
		return True

class OrderForm( forms.ModelForm ):
	class Meta:
		model = Order
		fields = ( 'uri', 'title', 'vendor', 'date', 'phase' )
		widgets = {
			'phase': forms.Select( choices = PHASES ),
		}
