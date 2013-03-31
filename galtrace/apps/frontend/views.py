from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from galtrace.apps.frontend.forms import RestoreForm, OrderForm
from galtrace.libs.core.models import PHASES


def index( request ):
	context = RequestContext( request )
	if not request.user.is_authenticated():
		return render_to_response( 'login.html', context )

	return redirect( 'galtrace.apps.frontend.views.member', user_name = request.user.username )

def member( request, user_name ):
	context = RequestContext( request )
	if not request.user.is_authenticated():
		# TODO show read only page
		return render_to_response( 'other.html', {
			'phases': PHASES,
		}, context_instance = context )

	if request.user.username != user_name:
		# TODO show read only page
		return render_to_response( 'other.html', {
			'phases': PHASES,
		}, context_instance = context )

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
			return redirect( 'galtrace.apps.frontend.views.index' )
		else:
			# redirect
			return redirect( 'galtrace.apps.frontend.views.index' )
	else:
		logout( request )
		return redirect( 'galtrace.apps.frontend.views.index' )

def csrf( request ):
	return render_to_response( 'csrf.js', {
	}, context_instance = RequestContext( request ), mimetype = 'text/javascript' )

def urls( request ):
	return render_to_response( 'urls.js', {
	}, context_instance = RequestContext( request ), mimetype = 'text/javascript' )

@login_required
def restore( request ):
	if request.method == 'POST':
		form = RestoreForm( data = request.POST, files = request.FILES )
		if form.is_valid():
			result = form.save( request.user )
	return redirect( index )
