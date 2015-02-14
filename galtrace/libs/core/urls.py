from django.conf.urls import patterns, url


urlpatterns = patterns('galtrace.libs.core.views',
    url(r'^load\.cgi$', 'load'),
    url(r'^save\.cgi$', 'save'),
    url(r'^move\.cgi$', 'move'),
    url(r'^delete\.cgi$', 'delete'),
    url(r'^backup\.cgi$', 'backup'),
    url(r'^fetch\.cgi$', 'fetch'),
)
