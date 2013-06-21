import json

from django import forms

from galtrace.libs.core.models import Order, PHASES

class RestoreForm( forms.Form ):
	data = forms.FileField()

	def save( self, user ):
		data_ = self.cleaned_data['data']
		data_ = json.load( data_ )
		return Order.objects.restore( user, data_ )

class OrderForm( forms.ModelForm ):
	class Meta:
		model = Order
		fields = ( 'uri', 'title', 'vendor', 'date', 'thumb', 'phase' )
		widgets = {
			'thumb': forms.TextInput(),
			'phase': forms.Select( choices = PHASES ),
		}

class EditForm( forms.Form ):
	title = forms.CharField()
	vendor = forms.CharField()
	date = forms.CharField()
	uri = forms.CharField()
	thumb = forms.CharField()

	def save( self, user, oldTitle ):
		title = self.cleaned_data['title']
		vendor = self.cleaned_data['vendor']
		date = self.cleaned_data['date']
		uri = self.cleaned_data['uri']
		thumb = self.cleaned_data['thumb']

		row = Order.objects.filter( user__exact = user, title__exact = oldTitle )
		if len( row ) != 1:
			return False
		row = row[0]
		row.title = title
		row.vendor = vendor
		row.date = date
		row.uri = uri
		row.retrieveThumb( thumb )
		row.save()

		return True
