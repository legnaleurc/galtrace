from django.conf.urls import patterns, url

urlpatterns = patterns( '',
	url( r'^$', 'kernel.views.index' ),
	url( r'^auth\.cgi$', 'kernel.views.auth' ),
	url( r'^csrf\.js$', 'kernel.views.csrf' ),
	url( r'^load\.cgi$', 'kernel.views.load' ),
	url( r'^save\.cgi$', 'kernel.views.save' ),
	url( r'^delete\.cgi$', 'kernel.views.delete' ),
	url( r'^backup\.cgi$', 'kernel.views.backup' ),
	url( r'^restore\.cgi$', 'kernel.views.restore' ),
	url( r'^fetch\.cgi$', 'kernel.views.fetch' ),
	url( r'^urls\.js$', 'kernel.views.urls' ),
	url( r'^robots\.txt$', 'kernel.views.robots' ),
)
