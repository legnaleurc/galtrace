from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'', include('galtrace.libs.core.urls')),
    url(r'', include('galtrace.apps.frontend.urls')),
)
