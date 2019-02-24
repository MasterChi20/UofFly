# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from . import unifier


def index(request):
	pairings = []
	
	if request.method != 'POST':
		pairings.append({
			'price': None,
			'flight_hour': None,
			'fuel': None,
			'airline': None,
			'rank': None,
			'bus_time': None
		})
		pairings.append({
			'price': None,
			'flight_hour': None,
			'fuel': None,
			'airline': None,
			'rank': None,
			'bus_time': None
		})
		pairings.append({
			'price': None,
			'flight_hour': None,
			'fuel': None,
			'airline': None,
			'rank': None,
			'bus_time': None
		})

	if request.method == 'POST':
		print(request.POST['departure_airport'])
		pairings = unifier.runner(request.POST['departure_airport'], request.POST['arrival_airport'], 
			request.POST['input_date'], float(request.POST['slider']), 100.0 - float(request.POST['slider']))

	context = {
    	'first': pairings[0],
    	'second': pairings[1],
    	'third': pairings[2]
    }
	return render(request, 'projectFly/index.html', context)

