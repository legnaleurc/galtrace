from django.conf.urls.defaults import patterns, url

urlpatterns = patterns( '',
	url( r'^$', 'main.views.index' ),
	url( r'^auth\.cgi$', 'main.views.auth' ),
	url( r'^csrf\.js$', 'main.views.csrf' ),
	url( r'^load\.cgi$', 'main.views.load' ),
	url( r'^save\.cgi$', 'main.views.save' ),
	url( r'^delete\.cgi$', 'main.views.delete' ),
	url( r'^backup\.cgi$', 'main.views.backup' ),
	url( r'^restore\.cgi$', 'main.views.restore' ),
	url( r'^fetch\.cgi$', 'main.views.fetch' ),
	url( r'^urls\.js$', 'main.views.urls' ),
)
