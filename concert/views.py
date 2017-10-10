# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Concert


# Create your views here.

def index(request):
    concert_list = get_list_or_404(Concert)
    template = loader.get_template('concert/index.html')
    context = {
        'concert_list': concert_list
    }
    print(context)
    return HttpResponse(template.render(context, request))

def technical(request, concertName):
    concer_list = Concert.objects.get(name=concertName)
    moreConcerts = len(concer_list) > 1

    return HttpResponse("<p>" +  str(concertName) + "</p>")