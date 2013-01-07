import re

from django.conf import settings
from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView


urlpatterns = patterns( '',
	url( r'^favicon\.ico|apple-touch-icon\.png$', RedirectView.as_view( url = '/static/favicon.ico' ) ),
	url( r'^robots\.txt$', RedirectView.as_view( url = '/static/robots.txt' ) ),
)

if not settings.DEBUG:
	urlpatterns[:0] = patterns( '',
		url( r'^{0}(?P<path>.*)$'.format( re.escape( settings.STATIC_URL.lstrip( '/' ) ) ), 'django.views.static.serve', {
			'document_root': settings.STATIC_ROOT,
			'show_indexes': False,
		} ),
	)
