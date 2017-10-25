# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Concert, Employment
from common.restrictions import GROUP_ID, group_access, restrict_access

# TODO: Veldig midlertidig, fiks snart!!!

#organiser = 1
#techician = 2
#manager = 3
#BOOKER_GROUP_ID = 4

#GROUP_ID = {'organiser': 1, 'techician': 2, 'manager': 3, 'BOOKER_GROUP_ID': 4}


# Create your views here.
"""
def group_access(user, *groups):
    for g in user.groups.all():
        if g.id in groups:
            return True

    return False
"""

def index(request):
    template = loader.get_template('concert/splash.html')
    context = {'organiser': group_access(request.user, GROUP_ID['organiser']) or request.user.is_superuser}
    return HttpResponse(template.render(context, request))


def techs(request):
    """

    :param request:
    :return:
    """

    user = request.user
    print("User: ", user)
    print("User ID: ", user.id)
    if not group_access(user, GROUP_ID['organiser']) and not user.is_superuser:
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
    """Generates list of concerts the user is responsible for/at.

    :param request: Request from client
    :returns: HTTPResponse with rendered my_concerts.html"""

    user = request.user

    if user.is_superuser or group_access(user, GROUP_ID['booker']):
        userType = GROUP_ID['booker']
        concerts = Concert.objects.all()
        tpl = 'concert/my_concerts.html'

    elif group_access(user, GROUP_ID['organiser']):
        userType = GROUP_ID['organiser']
        #TODO: Fix hardcoded year 2017
        concerts = Concert.objects.filter(time__year=2017)
        tpl = 'concert/my_concerts.html'

    elif group_access(user, GROUP_ID['techician']):
        userType = GROUP_ID['techician']
        concerts = []
        for employment in Employment.objects.filter(user=user.id):
            concerts.append(dict(concert=employment.concert, stage=employment.concert.stage, task=employment.task,
                                 time=employment.concert.time, needs=employment.concert.needs))
        tpl = 'concert/my_employments.html'
    else:
        return HttpResponse("NEI")
    """elif group_access(user, GROUP_ID['manager']):
        userType = GROUP_ID['manager']
        concerts = []
        for concert in Concert.objects.filter(band__manager_id=user.id):
            concert.append(dict(concert=concert.name, stage=concert.stage, time=concert.time, band=concert.band, ))
        tpl = 'concert/manager.html'"""



    template = loader.get_template(tpl)
    context = {'concerts': concerts, 'userType': userType}

    return HttpResponse(template.render(context, request))

@restrict_access([GROUP_ID['manager']])
def manager(request):
    """Generates HTML for managers

    :param request: HTTP Request (given by Django)
    :rtype: HttpResponse
    :returns: HTTPResponse rendered with concert/manager.html"""
    user = request.user

    userType = GROUP_ID['manager']
    concerts = []
    for concert in Concert.objects.filter(band__manager_id=user.id):
        concerts.append(dict(concert=concert.name, stage=concert.stage, time=concert.time, band=concert.band, needs=concert.needs))
    tpl = 'concert/manager.html'
    context = {'concerts': concerts, 'userType': userType}

    template = loader.get_template(tpl)

    return HttpResponse(template.render(context, request))