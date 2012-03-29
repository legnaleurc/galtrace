import json

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from main.models import Order, PHASES
from main.forms import RestoreForm, OrderForm
from main import sites

def ajaxView( f ):
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

@ajaxView
@require_POST
@login_required
def load( request ):
	offset = int( request.POST['offset'] )
	limit = offset + int( request.POST['limit'] )

	if offset < 0 or limit <= 0:
		raise ValueError( 'invalid interval' )

	result = Order.objects.filter( user__exact = request.user ).order_by( 'date', 'title' )[offset:limit].values()
	if len( result ) <= 0:
		return None
	else:
		result = [ x for x in result ]
		return result

@ajaxView
@require_POST
@login_required
def save( request ):
	args = getArgs( request )
	# title should not be null
	if u'title' not in args or len( args[u'title'] ) == 0:
		raise ValueError( '`title` is empty' )

	result = Order.objects.filter( title__exact = args[u'title'] )
	if( len( result ) == 0 ):
		# new item, insert
		result = Order( user = request.user, **args )
		result.save()
	else:
		# item exists, update
		result.update( **args )
		for x in result:
			x.save()

	return None

@ajaxView
@require_POST
@login_required
def delete( request ):
	args = getArgs( request )
	if u'title' not in args or len( args[u'title'] ) == 0:
		raise ValueError( '`title` is empty' )

	result = Order.objects.filter( title__exact = args[u'title'] )
	if( len( result ) == 0 ):
		raise RuntimeError( '{0} not found'.format( args[u'title'] ) )

	result[0].delete()
	return None

@login_required
def backup( request ):
	from datetime import datetime
	response = HttpResponse( content_type = 'text/plain; charset="utf-8"' )
	response['Content-Disposition'] = 'attachment; filename=galtrace_{0}.json'.format( datetime.now().strftime( '%Y%m%d%H%M%S' ) )
	data = Order.objects.dump( request.user )
	json.dump( data, response, ensure_ascii = False )
	return response

@login_required
def restore( request ):
	if request.method == 'POST':
		form = RestoreForm( data = request.POST, files = request.FILES )
		if form.is_valid():
			result = form.save( request.user )
	return redirect( index )

@ajaxView
@require_POST
@login_required
def fetch( request ):
	args = getArgs( request )
	result = sites.fetch( args[u'uri'] )
	return result
