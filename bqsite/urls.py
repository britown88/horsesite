from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
	url(r'^$', 'bqsite.views.index'),
	url(r'^changelog/?$', 'bqsite.views.changelog'),
	url(r'^charsim/?$', 'bqsite.views.charsim'),
	url(r'^charsim/update$', 'bqsite.views.csUpdate'),
	url(r'^charsim/addchar$', 'bqsite.views.csAddChar'),
)
