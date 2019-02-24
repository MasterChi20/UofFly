# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from . import unifier


def index(request):
    print(request.POST)
    pairings = unifier.runner("Chicago", "Dubai", "04/04/2019", 1.0, 0.0)
    context = {
    	'first': pairings[0],
    	'second': pairings[1],
    	'third': pairings[2]
    }
    return render(request, 'projectFly/index.html', context)

