# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Concert, Employment


# TODO: Veldig midlertidig, fiks snart!!!

ORGANISER_GROUP_ID = 1
TECHNICIAN_GROUP_ID = 2
MANAGER_GROUP_ID = 3
BOOKER_GROUP_ID = 4

# Create your views here.

def group_access(user, *groups):
    for g in user.groups.all():
        if g.id in groups:
            return True

    return False


def index(request):
    template = loader.get_template('concert/splash.html')
    context = {'organiser': group_access(request.user, ORGANISER_GROUP_ID) or request.user.is_superuser}
    return HttpResponse(template.render(context, request))


def techs(request):
    user = request.user
    print("User: ", user)
    print("User ID: ", user.id)
    if not group_access(user, ORGANISER_GROUP_ID) and not user.is_superuser:
            return HttpResponse(False)

    if user.is_superuser:
        concerts = Concert.objects.all()
    else:
        concerts = Concert.objects.filter(organiser=user.id)

    employments = []
    for concert in concerts:
        for tech in concert.techs.all():
            employments.append({
                'concert': concert.name[:32],
                'stage': concert.stage.name[:32],
                'tech': tech,
                'task': Employment.objects.get(concert=concert, user=tech),
                'time': concert.time,})


    template = loader.get_template('concert/my_technicians.html')
    context = {'employments': employments}

    ret = ''
    for concert in concerts:
        ret += '<p>' + concert.name + '</p>'
    groups = request.user.groups.all()


    #template.render(context, request)
    return HttpResponse(template.render(context, request))

def concerts(request):
    user = request.user

    if user.is_superuser or group_access(user, BOOKER_GROUP_ID):
        concerts = Concert.objects.all()
        tpl = 'concert/my_concerts.html'
    elif group_access(user, ORGANISER_GROUP_ID):
        concerts = Concert.objects.filter(time__year=2017)
        tpl = 'concert/my_concerts.html'
    elif group_access(user, TECHNICIAN_GROUP_ID):
        concerts = []
        for employment in Employment.objects.filter(user=user.id):
            concerts.append({
                'concert': employment.concert,
                'stage': employment.concert.stage,
                'task': employment.task,
                'time': employment.concert.time,
                'needs': employment.concert.needs})
        tpl = 'concert/my_employments.html'
    else:
        return HttpResponse("NEI")

    template = loader.get_template(tpl)
    context = {'concerts': concerts}

    return HttpResponse(template.render(context, request))


