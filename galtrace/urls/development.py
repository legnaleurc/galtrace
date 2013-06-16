from django.conf import settings
from django.conf.urls.static import static

from . import *


urlpatterns[:0] = static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT )
