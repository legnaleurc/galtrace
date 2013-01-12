from django.conf.urls import patterns, url

urlpatterns = patterns( 'galtrace.apps.frontend.views',
	url( r'^$', 'index' ),
	url( r'^auth\.cgi$', 'auth' ),
	url( r'^csrf\.js$', 'csrf' ),
	url( r'^urls\.js$', 'urls' ),
	url( r'^restore\.cgi$', 'restore' ),
	url( r'^(?P<user_name>.+)$', 'member' ),
)
