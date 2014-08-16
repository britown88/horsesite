# Create your views here.
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect

import time
import multiprocessing


def getLines():
	file = open('/home/btownsen/gitrepos/todo-helper/todo.log', 'r')
	lines = file.readlines()
	file.close()
	return lines

def index(request):
	return render_to_response('dhsite/index.html')

import re

def zendesk(request):
	return render_to_response('zendesk_tab.html')

def gitstats(request, fname):
	return render_to_response('dhsite/gitstats/'+fname)

def addSpans(lines):
	spanLines = []
	for line in lines:
		spanClass = re.compile('\[(.*?)\]').findall(line)[0]
		spanLines.append("<span class=%s>%s</span>" % (spanClass, line))
	return spanLines

def amishHome(request):
	if request.is_ajax():
		lines = getLines()
		data = {}
		t = time.localtime()
		min = t.tm_min
		sec = t.tm_sec
		
		minToHr = 60 - min
		minToHfHr = 30 - min + (60 if min > 30 else 0)
		finalMin = minToHr if minToHr < minToHfHr else minToHfHr
		
		finalSec = 60 - sec if sec > 0 else 0		
		if finalSec > 0:
			finalMin -= 1
		
		data['minTillUpdate'] = finalMin
		data['secTillUpdate'] = finalSec
		
		data['lineCount'] = len(lines)
		data['lines'] = lines[-10:]
		data['allowUpdate'] = (lines[len(lines)-1].count('[Done]') > 0)
		return HttpResponse(simplejson.dumps(data), mimetype="application/json")

		
	
	return render_to_response('amish/index.html') 

def amishGetLineCount(request):
	if request.is_ajax():		
		d = {'lineCount':len(getLines())}
		return HttpResponse(simplejson.dumps(d), mimetype="application/json")
	return HttpResponseRedirect('/amishbot/')

def amishTerminate(request):

	return HttpResponseRedirect('/amishbot/')

import subprocess

def amishUpdate(request):
	return HttpResponseRedirect('/amishbot/')
