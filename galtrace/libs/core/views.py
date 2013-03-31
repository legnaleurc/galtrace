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
	args = {}
	for item in request.POST.iteritems():
		if item[0] in [ u'phase', u'volume' ]:
			args[item[0]] = int( item[1] )
		else:
			args[item[0]] = item[1]
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

	result = Order.objects.filter( user__exact = user ).order_by( 'date', 'title' )[offset:limit].values()
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

@require_POST
@login_required
@ajaxView
def fetch( request ):
	args = getArgs( request )
	result = crawler.fetch( args[u'uri'] )
	return result
