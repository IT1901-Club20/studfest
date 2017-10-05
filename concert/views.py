# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Concert


# Create your views here.

def index(request):
    concert = get_object_or_404(Concert, )
    template = loader.get_template('concert/index.html')
    context = {
        'concert': concert
    }
    print(context)
    return HttpResponse(template.render(context, request))
