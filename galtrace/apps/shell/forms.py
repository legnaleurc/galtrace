#-*- coding: utf-8 -*-

import json

from django import forms

from galtrace.apps.shell.models import Order, PHASES

class RestoreForm( forms.Form ):
	data = forms.FileField()

	def save( self, user ):
		data_ = self.cleaned_data['data']
		data_ = json.load( data_ )
		return Order.objects.restore( user, data_ )

class OrderForm( forms.ModelForm ):
	class Meta:
		model = Order
		fields = ( 'uri', 'title', 'vendor', 'date', 'phase' )
		widgets = {
			'phase': forms.Select( choices = PHASES ),
		}