# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Concert


# TODO: Veldig midlertidig, fiks snart!!!

ORGANISER_GROUP_ID = 1

# Create your views here.

def group_access(user, *groups):
    for g in user.groups.all():
        if g.id in groups:
            return True

    return False


def index(request):
    concertList = Concert.objects.all()

    template = loader.get_template('concert/index.html')
    context = {
        'concertList': concertList
    }
    print(concertList[0].name)
    return HttpResponse(template.render(context, request))


def techs(request):
    user = request.user
    print("User: ", user)
    print("User ID: ", user.id)
    if not group_access(user, ORGANISER_GROUP_ID) and not user.is_superuser:
            return HttpResponse(False)

    if user.is_superuser:
        # TODO: Sjå på kvifor dette ikkje funkar
        concerts = Concert.objects.all()
    else:
        concerts = Concert.objects.filter(organiser=user.id)

    employments = []
    for concert in concerts:
        for tech in concert.techs.all():
            employments.append({'concert': concert.name[:32], 'tech': tech})


    template = loader.get_template('concert/techs.html')

    context = {'employments': employments}

    ret = ''
    for concert in concerts:
        ret += '<p>' + concert.name + '</p>'
    groups = request.user.groups.all()


    #template.render(context, request)
    return HttpResponse(template.render(context, request))