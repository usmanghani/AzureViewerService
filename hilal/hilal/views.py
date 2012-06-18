from django.http import HttpResponse
from BeautifulSoup import BeautifulSoup
from django.core import serializers
from praytimes import PrayTimes
from datetime import date, timedelta

import requests
import simplejson

p = PrayTimes('Karachi')
p.setMethod('Karachi')
p.adjust({'asr':'Hanafi'})

def pray(request, location):
	if location:
		r = requests.get('http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false' % location)
		geocode = simplejson.loads(r.text)

		address = geocode['results'][0]['formatted_address']
		loc = geocode['results'][0]['geometry']['location']
		lat = loc['lat']
		lng = loc['lng']
		
		requested_date = date.today()
		times = p.getTimes(requested_date, (lat, lng), -8, True)
		response = {'date' : requested_date.strftime("%Y-%m-%d"), 'address': address, 'latitude' : lat, 'longitude' : lng, 'times': times}

		return HttpResponse(simplejson.dumps(response), content_type='application/json')
	else:
		return HttpResponse(status=400)

def pray_date(request, year, month, day, location):
	try:
		if location:
			r = requests.get('http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false' % location)
			geocode = simplejson.loads(r.text)

			address = geocode['results'][0]['formatted_address']
			loc = geocode['results'][0]['geometry']['location']
			lat = loc['lat']
			lng = loc['lng']

			requested_date = date(int(year), int(month), int(day))
			
			times = p.getTimes(requested_date, (lat, lng), -8, True)
			
			response = {'date':requested_date.strftime("%Y-%m-%d"), 'month':month, 'day':day, 'address': address, 'latitude' : lat, 'longitude' : lng, 'times' : times}

			return HttpResponse(simplejson.dumps(response), content_type='application/json')
		else:
			return HttpResponse(status=400)
	except:
		return HttpResponse(status=400)

def pray_month(request, year, month, location):
	try:
		if location:
			r = requests.get('http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false' % location)
			geocode = simplejson.loads(r.text)

			address = geocode['results'][0]['formatted_address']
			loc = geocode['results'][0]['geometry']['location']
			lat = loc['lat']
			lng = loc['lng']

			start_date = date(year=int(year), month=int(month), day=1)
			end_date = date(year=int(year), month=(int(month) + 1), day=1)
			
			day_count = (end_date - start_date).days + 1
			
			response = []
			for single_date in [d for d in (start_date + timedelta(n) for n in range(day_count)) if d < end_date]:
				times = p.getTimes(single_date, (lat, lng), -8, True)
				response.append({'date':single_date.strftime("%Y-%m-%d"), 'address': address, 'latitude' : lat, 'longitude' : lng, 'times' : times})

			return HttpResponse(simplejson.dumps(response), content_type='application/json')
		else:
			return HttpResponse(status=400)
	except:
		return HttpResponse(status=400)

def pray_year(request, year, location):
	try:
		if location:
			r = requests.get('http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false' % location)
			geocode = simplejson.loads(r.text)

			address = geocode['results'][0]['formatted_address']
			loc = geocode['results'][0]['geometry']['location']
			lat = loc['lat']
			lng = loc['lng']

			start_date = date(year=int(year), month=1, day=1)
			end_date = date(year=int(year) + 1, month=1, day=1)

			day_count = (end_date - start_date).days + 1
			
			response = []
			for single_date in [d for d in (start_date + timedelta(n) for n in range(day_count)) if d < end_date]:
				times = p.getTimes(single_date, (lat, lng), -8, True)
				response.append({'date':single_date.strftime("%Y-%m-%d"), 'address': address, 'latitude' : lat, 'longitude' : lng, 'times' : times})

			return HttpResponse(simplejson.dumps(response), content_type='application/json')
		else:
			return HttpResponse(status=400)
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