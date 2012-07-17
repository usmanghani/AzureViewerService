from django.http import HttpResponse
from BeautifulSoup import BeautifulSoup
from django.core import serializers
import requests
import simplejson

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