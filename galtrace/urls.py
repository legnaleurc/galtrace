from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns( '',
	url( r'^favicon\.ico|apple-touch-icon\.png$', RedirectView.as_view( url = '/static/favicon.ico' ) ),
	url( r'^robots\.txt$', RedirectView.as_view( url = '/static/robots.txt' ) ),

	# url( r'^admin/doc/', include( 'django.contrib.admindocs.urls' ) ),
	# url( r'^admin/', include( admin.site.urls ) ),

	url( r'', include( 'kernel.urls' ) ),
)

from django.conf import settings
import re

if not settings.DEBUG:
	urlpatterns += patterns( '',
		url( r'^{0}(?P<path>.*)$'.format( re.escape( settings.STATIC_URL.lstrip( '/' ) ) ), 'django.views.static.serve', {
			'document_root': settings.STATIC_ROOT,
			'show_indexes': False,
		} ),
	)
