import re

from django.conf import settings
from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView


urlpatterns = patterns( '',
	url( r'^favicon\.ico|apple-touch-icon\.png$', RedirectView.as_view( url = '/static/favicon.ico' ) ),
	url( r'^robots\.txt$', RedirectView.as_view( url = '/static/robots.txt' ) ),
)

urlpatterns += patterns( 'galtrace.libs.core.views',
	url( r'^load\.cgi$', 'load' ),
	url( r'^save\.cgi$', 'save' ),
	url( r'^move\.cgi$', 'move' ),
	url( r'^delete\.cgi$', 'delete' ),
	url( r'^backup\.cgi$', 'backup' ),
	url( r'^fetch\.cgi$', 'fetch' ),
)

if not settings.DEBUG:
	urlpatterns[:0] = patterns( '',
		url( r'^{0}(?P<path>.*)$'.format( re.escape( settings.STATIC_URL.lstrip( '/' ) ) ), 'django.views.static.serve', {
			'document_root': settings.STATIC_ROOT,
			'show_indexes': False,
		} ),
	)
