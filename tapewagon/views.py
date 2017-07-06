# Create your views here.
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt

import urllib
import urllib2
import random

def index(request):
	return render_to_response('tapewagon/index.html')
