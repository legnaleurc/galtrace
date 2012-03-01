from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns( '',
	# Examples:
	# url(r'^$', 'cart.views.home', name='home'),
	# url(r'^cart/', include('cart.foo.urls')),
	url( r'^', include( 'main.urls' ) ),
#	url( r'^accounts', 'django.contrib.auth.urls' ),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url( r'^admin/', include( admin.site.urls ) ),
)

urlpatterns += staticfiles_urlpatterns()
