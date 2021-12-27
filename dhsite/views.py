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
	return render_to_response('dhsite/index.html')

def ddash(request):
    return render_to_response('ddash/index.html')

def pointbuy(request):
    return render_to_response('dhsite/pointbuy.html')

def exodus(request):
    return render_to_response('dhsite/exodus.html')

def websight(request):
    return render_to_response('dhsite/websight.html')

@csrf_exempt
def exodusUpdate(request):
    if request.is_ajax():
        label = request.POST['name']

        x = random.randint(0, 1000)
        y = random.randint(0, 1000)
        z = random.randint(0, 1000)

        command = "(create-label (point %d %d %d) \"%s\" :name \"%s\")"%(x, y, z, label, label)

        urllib2.urlopen("http://studio-horse.com:8000/send/"+urllib.quote(command))

        return HttpResponse(simplejson.dumps({}), mimetype="application/json")

    return render_to_response('dhsite/exodus.html')



