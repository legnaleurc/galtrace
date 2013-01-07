from django.conf.urls import patterns, url

urlpatterns = patterns( 'galtrace.apps.shell.views',
	url( r'^$', 'index' ),
	url( r'^auth\.cgi$', 'auth' ),
	url( r'^csrf\.js$', 'csrf' ),
	url( r'^load\.cgi$', 'load' ),
	url( r'^save\.cgi$', 'save' ),
	url( r'^move\.cgi$', 'move' ),
	url( r'^delete\.cgi$', 'delete' ),
	url( r'^backup\.cgi$', 'backup' ),
	url( r'^restore\.cgi$', 'restore' ),
	url( r'^fetch\.cgi$', 'fetch' ),
	url( r'^urls\.js$', 'urls' ),
	url( r'^(?P<user_name>.+)$', 'member' ),
)
