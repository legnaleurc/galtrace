import json

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse

from main.models import Order, OrderForm, PHASES
from main import sites

def index( request ):
	context = RequestContext( request )
	if not request.user.is_authenticated():
		return render_to_response( 'index.html', context )

	form = OrderForm()
	items = Order.objects.all().filter( user__exact = request.user ).order_by( 'date', 'title' ).values()
	return render_to_response( 'index.html', { 'phases': PHASES, 'form': form, 'items': items }, context_instance = context )

def auth( request ):
	from django.contrib.auth import authenticate, login, logout
	userName = request.POST[u'user'] if u'user' in request.POST else ''
	password = request.POST[u'pswd'] if u'user' in request.POST else ''
	user = authenticate( username = userName, password = password )
	if user is not None:
		if user.is_active:
			login( request, user )
			# redirect
			return redirect( 'main.views.index' )
		else:
			# redirect
			return redirect( 'main.views.index' )
	else:
		logout( request )
		return redirect( 'main.views.index' )

def csrf( request ):
	return render_to_response( 'csrf.js', {}, context_instance = RequestContext( request ), mimetype = 'text/javascript' )

def getArgs( request ):
	args = {}
	for item in request.POST.items():
		if item[0] in [ u'phase', u'volume' ]:
			args[item[0]] = int( item[1] )
		else:
			args[item[0]] = item[1]
	return args

def load( request ):
	result = Order.objects.all().order_by( 'date', 'title' ).values()
	result = [ x for x in result ]
	return HttpResponse( json.dumps( result ), content_type = 'text/plain; charset="utf-8"' )

def save( request ):
	args = getArgs( request )
	# title should not be null
	if u'title' not in args or len( args[u'title'] ) == 0:
		return HttpResponse( json.dumps( '`title` is empty' ), content_type = 'text/plain; charset="utf-8"' )

	result = Order.objects.filter( title__exact = args[u'title'] )
	if( len( result ) == 0 ):
		# new item, insert
		result = Order( **args )
		result.save()
	else:
		# item exists, update
		result.update( **args )
		for x in result:
			x.save()

	return HttpResponse( content_type = 'text/plain; charset="utf-8"' )

def delete( request ):
	args = getArgs( request )
	if u'title' not in args or len( args[u'title'] ) == 0:
		return HttpResponse( json.dumps( '`title` is empty' ), content_type = 'text/plain; charset="utf-8"' )

	result = Order.objects.filter( title__exact = args[u'title'] )
	if( len( result ) == 0 ):
		return HttpResponse( json.dumps( '{0} not found'.format( args[u'title'] ) ), content_type = 'text/plain; charset="utf-8"' )

	result[0].delete()
	return HttpResponse( content_type = 'text/plain; charset="utf-8"' )

def dump( request ):
	from django.core import serializers
	response = HttpResponse( content_type = 'text/plain; charset="utf-8"' )
	response['Content-Disposition'] = 'attachment; filename=cart.json'
	s = serializers.get_serializer( 'json' )()
	result = Order.objects.all()
	s.serialize( result, stream = response )
	return response

def fetch( request ):
	args = getArgs( request )
	result = sites.fetch( args[u'uri'] )
	return HttpResponse( json.dumps( result ), content_type = 'text/plain; charset="utf-8"' )
