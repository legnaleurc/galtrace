import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from galtrace.libs import crawler
from galtrace.libs.core.models import Order, PHASES


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
				'message': unicode( e ),
			} )
	return g

def getArgs( request ):
	from django.utils.html import escape, strip_tags
	args = {}
	for k, v in request.POST.items():
		if k in ( u'phase', u'volume' ):
			args[k] = int( v )
		else:
			# NOTE strip HTML tags and escape contents
			args[k] = escape( strip_tags( v ) )
	return args


@require_POST
@ajaxView
def load( request ):
	offset = int( request.POST['offset'] )
	limit = offset + int( request.POST['limit'] )
	user = request.POST['user_id']

	if offset < 0 or limit <= 0:
		raise ValueError( 'invalid interval' )

	from django.contrib.auth.models import User
	try:
		user = User.objects.get( username__exact = user )
	except User.DoesNotExist:
		raise ValueError( u'user \'{0}\' does not exist'.format( user ) )
	except User.MultipleObjectsReturned:
		raise ValueError( 'user database corrupted' )

	result = Order.objects.filter( user__exact = user ).order_by( 'date', 'title' )[offset:limit]
	if not result:
		return None
	else:
		result = [ {
			u'title': x.title,
			u'vendor': x.vendor,
			u'date': x.date,
			u'uri': x.uri,
			u'thumb': u'' if not x.thumb else x.thumb.url,
			u'phase': x.phase,
			u'volume': x.volume,
		} for x in result ]
		return result

@require_POST
@login_required
@ajaxView
def save( request ):
	args = getArgs( request )

	# purify keys
	args = { k: args[k] for k in ( u'title', u'new_title', u'vendor', u'date', u'uri', u'thumb', u'phase', u'volume' ) if k in args }

	# title should not be null
	if not args[u'title']:
		raise ValueError( u'`title` is empty' )

	newTitle = None
	if u'new_title' in args:
		newTitle = args[u'new_title']
		del args[u'new_title']

	thumbUri = None
	if u'thumb' in args:
		thumbUri = args[u'thumb']
		del args[u'thumb']

	try:
		result = Order.objects.get( user__exact = request.user, title__exact = args[u'title'] )
		del args[u'title']
		# item exists, update
		for k in args:
			setattr( result, k, args[k] )
		if newTitle:
			result.title = newTitle
	except Order.DoesNotExist:
		# new item, insert
		result = Order( user = request.user, **args )
		result.retrieveThumb( thumbUri )
	except Order.MultipleObjectsReturned:
		# TODO new exception
		raise

	result.save()
	return {
		u'title': result.title,
		u'vendor': result.vendor,
		u'date': result.date,
		u'uri': result.uri,
		u'thumb': u'' if not result.thumb else result.thumb.url,
		u'phase': result.phase,
		u'volume': result.volume,
	}

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

@require_POST
@login_required
@ajaxView
def fetch( request ):
	args = getArgs( request )
	result = crawler.fetch( args[u'uri'] )
	return result
