from django.http import HttpResponse
from BeautifulSoup import BeautifulSoup
from django.core import serializers
from praytimes import PrayTimes
from datetime import date, timedelta
from math import floor
from lxml import objectify
from lxml import etree

import os
import os.path
import requests
import simplejson

DEFAULT_METHOD = 'Karachi'
DEFAULT_ASR = 'Hanafi'

p = PrayTimes(DEFAULT_METHOD)
p.setMethod(DEFAULT_METHOD)
p.adjust({'asr':DEFAULT_ASR})

def timezone(lat, lng):
	r = requests.get("http://api.geonames.org/timezoneJSON?lat=%s&lng=%s&username=usmanghani" % (lat, lng))
	json = simplejson.loads(r.text)

	rawOffset = json['rawOffset']
	dstOffset = json['dstOffset']
	dst = rawOffset != dstOffset

	# r = requests.get("http://www.earthtools.org/timezone/%s/%s" % (lat, lng))
	# root = objectify.fromstring(r.text.encode('ascii'))
	
	# dst = False
	# if root.dst == 'Unknown':
	# 	dst = False
	# else:
	# 	dst = bool(root.dst)

	# return int(root.offset), dst  
	return int(rawOffset), dst

def calculate_pray(start_date, end_date, location, method, asr_method):
	try:
		if location:
			p.setMethod(method)
			p.adjust({'asr':asr_method})
			r = requests.get('http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false' % location)
			geocode = simplejson.loads(r.text)

			address = geocode['results'][0]['formatted_address']
			loc = geocode['results'][0]['geometry']['location']
			lat = loc['lat']
			lng = loc['lng']
			
			day_count = (end_date - start_date).days + 1
			# import pdb; pdb.set_trace()
			offset, dst = timezone(lat, lng)

			response = []
			for single_date in [d for d in (start_date + timedelta(n) for n in range(day_count)) if d < end_date]:
				times = p.getTimes(single_date, (lat, lng), offset, dst)
				response.append({'date':single_date.strftime("%Y-%m-%d"), 'address': address, 'latitude' : lat, 'longitude' : lng, 'method': method, 'asr_method' : asr_method, 'offset' : offset, 'dst' : dst, 'times' : times})

			return HttpResponse(simplejson.dumps(response), content_type='application/json')
		else:
			return HttpResponse(status=400)
	except:
		return HttpResponse(status=400)

def pray(request, location):
	try:
		method = request.GET.get('method', DEFAULT_METHOD)
		asr_method = request.GET.get('asr', DEFAULT_ASR)
		return calculate_pray(date.today(), date.today() + timedelta(1), location, method, asr_method)
	except:
		return HttpResponse(status=400)

def pray_date(request, year, month, day, location):
	try:
		requested_date = date(int(year), int(month), int(day))
		method = request.GET.get('method', DEFAULT_METHOD)
		asr_method = request.GET.get('asr', DEFAULT_ASR)
		return calculate_pray(requested_date, requested_date + timedelta(1), location, method, asr_method)
	except:
		return HttpResponse(status=400)

def pray_month(request, year, month, location):
	try:
		start_date = date(year=int(year), month=int(month), day=1)
		end_date = date(year=int(year), month=(int(month) + 1), day=1)
		method = request.GET.get('method', DEFAULT_METHOD)
		asr_method = request.GET.get('asr', DEFAULT_ASR)
		return calculate_pray(start_date, end_date, location, method, asr_method)
	except:
		return HttpResponse(status=400)

def pray_year(request, year, location):
	try:
		start_date = date(year=int(year), month=1, day=1)
		end_date = date(year=int(year) + 1, month=1, day=1)
		method = request.GET.get('method', DEFAULT_METHOD)
		asr_method = request.GET.get('asr', DEFAULT_ASR)
		return calculate_pray(start_date, end_date, location, method, asr_method)
	except:
		return HttpResponse(status=400)

def hilal(request, month):
	r = requests.get('http://chicagohilal.org');
	soup = BeautifulSoup(r.text)
	div = soup.findAll('div', {'id':'accordion'})
	uls = div[0].findAll('ul')
	lis = uls[0].findAll('li')
	lookup = {}
	for li in lis:
		hilal = li.findAll('a')[1].string
		start_date = li.findAll('span')[0].string
		lookup[hilal] = start_date
	keys = set()
	if month:
		input_str = month
		for hilal in lookup.keys():
			hilal_lower = hilal.lower()
			found = True
			for input in input_str.split(' '):
				# import pdb; pdb.set_trace()
				if not input:
					continue
				index = hilal_lower.find(input.lower())
				found = found & (index > -1)
				# if index > -1:
				# 	found = True
				# else:
				# 	found = False
			if found:
				keys.add(hilal)
	else:
		keys = lookup.keys()
	
	response = [{key : lookup[key]} for key in keys]
	return HttpResponse(simplejson.dumps(response), content_type='application/json')

def hilal_index(request):
	return hilal(request, month='')

def home(request):
	with open(os.path.join(os.path.dirname(__file__), 'static/docs.html')) as docs:
		return HttpResponse(docs.read())

