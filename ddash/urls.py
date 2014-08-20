from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    url(r'^$', 'ddash.views.index'),
)
