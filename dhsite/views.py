# Create your views here.
from django.shortcuts import render_to_response

def index(request):
	return render_to_response('dhsite/index.html')

def ddash(request):
    return render_to_response('ddash/index.html')
    
def pointbuy(request):
    return render_to_response('dhsite/pointbuy.html')

