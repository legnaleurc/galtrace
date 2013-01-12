from django.conf.urls import patterns, include, url

from . import *


urlpatterns[:0] = patterns( '',
	url( r'', include( 'galtrace.apps.backend.urls' ) ),
)
