import re
from django.conf import settings


class SubdomainsMiddleware:
    def process_request(self, request):
	try:
	    hostname = request.META['HTTP_HOST']
	    for key in settings.URLCONF.iterkeys():
		match = re.search(key, hostname)
		if(match):
		    request.urlconf = settings.URLCONF[key]
		    break

	except (KeyError, AttributeError):
	    request.urlconf = 'dhsite.urls'
	    pass

	return None
#	request.urlconf = request.get_host().split('.')[0] == 'bladequest' ? 'bqsite.urls' : 'dhsite.urls'

#        request.domain = request.META['HTTP_HOST']
#        request.subdomain = ''
#        parts = request.domain.split('.')
#
#        # blog.101ideas.cz or blog.localhost:8000
#        if len(parts) == 3 or (re.match("^localhost", parts[-1]) and len(parts) == 2):
#            request.subdomain = parts[0]
#            request.domain = '.'.join(parts[1:])
#
#        # set the right urlconf
#        if request.subdomain == 'bladequest':
#            request.urlconf = 'bqsite.urls'
#        else:
#            request.urlconf = 'dhsite.urls'


