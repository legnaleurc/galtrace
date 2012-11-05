import json

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from kernel.models import Order, PHASES
from kernel.forms import RestoreForm, OrderForm
import crawler

def ajaxView( f ):
	'''
	This decorator serialize returning object to JSON.
	All exceptions will be catched and serialized.
	For the contrast to Django, this decorator must be the most inner one.

	Keyword arguments:
	f -- the view which returns as an object
	'''
	def toJSONResponse( x ):
		return HttpResponse( json.dumps( x ), content_type = 'text/plain; charset="utf-8"' )
	def g( request ):
		try:
			return toJSONResponse( {
				'success': True,
				'data': f( request ),
			} )
		except Exception as e:
			return toJSONResponse( {
				'success': False,
				'type': e.__class__.__name__,
				'message': e.message,
			} )
	return g

def index( request ):
	context = RequestContext( request )
	if not request.user.is_authenticated():
		return render_to_response( 'login.html', context )

	return redirect( 'kernel.views.member', user_name = request.user.username )

def member( request, user_name ):
	context = RequestContext( request )
	if not request.user.is_authenticated():
		# TODO show read only page
		return redirect( 'kernel.views.index' )

	if request.user.username != user_name:
		# TODO show read only page
		return redirect( 'kernel.views.index' )

	form = OrderForm()
	restoreForm = RestoreForm()
	return render_to_response( 'self.html', {
		'phases': PHASES,
		'form': form,
		'restoreForm': restoreForm,
	}, context_instance = context )

def auth( request ):
	from django.contrib.auth import authenticate, login, logout
	userName = request.POST[u'user'] if u'user' in request.POST else ''
	password = request.POST[u'pswd'] if u'user' in request.POST else ''
	user = authenticate( username = userName, password = password )
	if user:
		if user.is_active:
			login( request, user )
			# redirect
			return redirect( 'kernel.views.index' )
		else:
			# redirect
			return redirect( 'kernel.views.index' )
	else:
		logout( request )
		return redirect( 'kernel.views.index' )

def csrf( request ):
	return render_to_response( 'csrf.js', {
	}, context_instance = RequestContext( request ), mimetype = 'text/javascript' )

def urls( request ):
	return render_to_response( 'urls.js', {
	}, context_instance = RequestContext( request ), mimetype = 'text/javascript' )

def getArgs( request ):
	args = {}
	for item in request.POST.items():
		if item[0] in [ u'phase', u'volume' ]:
			args[item[0]] = int( item[1] )
		else:
			args[item[0]] = item[1]
	return args

@require_POST
@login_required
@ajaxView
def load( request ):
	offset = int( request.POST['offset'] )
	limit = offset + int( request.POST['limit'] )

	if offset < 0 or limit <= 0:
		raise ValueError( 'invalid interval' )

	result = Order.objects.filter( user__exact = request.user ).order_by( 'date', 'title' )[offset:limit].values()
	if not result:
		return None
	else:
		result = [ x for x in result ]
		return result

@require_POST
@login_required
@ajaxView
def save( request ):
	args = getArgs( request )
	# title should not be null
	if u'title' not in args or not args[u'title']:
		raise ValueError( '`title` is empty' )

	result = Order.objects.filter( title__exact = args[u'title'] )
	if not result:
		# new item, insert
		result = Order( user = request.user, **args )
		result.save()
	else:
		# item exists, update
		result.update( **args )

	return None

@require_POST
@login_required
@ajaxView
def move( request ):
	phase = int( request.POST[u'phase'] )
	orders = request.POST.getlist( u'orders[]' )

	result = Order.objects.filter( title__in = orders )
	result.update( phase = phase )

	return None

@require_POST
@login_required
@ajaxView
def delete( request ):
	orders = request.POST.getlist( u'orders[]' )
	if not orders:
		raise ValueError( u'empty request' )

	result = Order.objects.filter( title__in = orders )
	if not result:
		raise ValueError( u'no order matched' )

	result.delete()

	return None

@login_required
def backup( request ):
	from datetime import datetime
	response = HttpResponse( content_type = 'text/plain; charset="utf-8"' )
	response['Content-Disposition'] = 'attachment; filename=galtrace_{0}.json'.format( datetime.now().strftime( '%Y%m%d%H%M%S' ) )
	data = Order.objects.dump( request.user )
	json.dump( data, response, ensure_ascii = False, separators = ( ',', ':' ) )
	return response

@login_required
def restore( request ):
	if request.method == 'POST':
		form = RestoreForm( data = request.POST, files = request.FILES )
		if form.is_valid():
			result = form.save( request.user )
	return redirect( index )

@require_POST
@login_required
@ajaxView
def fetch( request ):
	args = getArgs( request )
	result = crawler.fetch( args[u'uri'] )
	return result

def robots( request ):
	response = HttpResponse( mimetype = 'text/plain' )
	response.write( 'User-agent: *\n' )
	response.write( 'Disallow: /\n' )
	return response
