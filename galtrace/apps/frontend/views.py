from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from galtrace.apps.frontend.forms import EditorForm, OrderForm, RestoreForm
from galtrace.libs.core.models import PHASES


def index( request ):
	context = RequestContext( request )
	if not request.user.is_authenticated():
		return render_to_response( 'login.html', context )

	return redirect( 'galtrace.apps.frontend.views.member', user_name = request.user.username )

def member( request, user_name ):
	context = RequestContext( request )
	if not request.user.is_authenticated():
		return render_to_response( 'other.html', {
			'phases': PHASES,
		}, context_instance = context )

	if request.user.username != user_name:
		return render_to_response( 'other.html', {
			'phases': PHASES,
		}, context_instance = context )

	form = OrderForm()
	editForm = EditorForm()
	restoreForm = RestoreForm()
	return render_to_response( 'self.html', {
		'phases': PHASES,
		'form': form,
		'editForm': editForm,
		'restoreForm': restoreForm,
	}, context_instance = context )

def auth( request ):
	from django.contrib.auth import authenticate, login, logout
	userName = request.POST.get( u'user', '' )
	password = request.POST.get( u'pswd', '' )
	nextPage = request.GET.get( u'next', u'/' )

	user = authenticate( username = userName, password = password )
	if user:
		if user.is_active:
			login( request, user )
			# redirect
			return redirect( nextPage )
		else:
			# TODO show error message
			return redirect( 'galtrace.apps.frontend.views.index' )
	else:
		logout( request )
		return redirect( nextPage )

def csrf( request ):
	return render_to_response( 'csrf.js', {
	}, context_instance = RequestContext( request ), content_type = 'text/javascript' )

def urls( request ):
	return render_to_response( 'urls.js', {
	}, context_instance = RequestContext( request ), content_type = 'text/javascript' )

@login_required
def restore( request ):
	if request.method == 'POST':
		form = RestoreForm( data = request.POST, files = request.FILES )
		if form.is_valid():
			result = form.save( request.user )
	return redirect( index )
