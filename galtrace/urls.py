from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns( '',
	url( r'', include( 'kernel.urls' ) ),
	url( r'^favicon\.ico|apple-touch-icon\.png$', 'django.views.generic.simple.redirect_to', {
		'url': '/static/img/favicon.ico',
	} ),

	# url( r'^admin/doc/', include( 'django.contrib.admindocs.urls' ) ),
	url( r'^admin/', include( admin.site.urls ) ),
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
