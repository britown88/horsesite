import os
import sys

path = '/srv/website'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'website.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
