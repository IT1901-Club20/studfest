"""Studfests concert-app

Renders html-pages based on user. Permission-restriction done through @restrict-access decorator.
Functions:
*Index(request)
*techs(request)
*concerts(request)
*manager(request)
"""
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Concert, Employment
from common.restrictions import GROUP_ID, group_access, allow_access
from . import concertNeedsForm


def index(request):
    """Renders front-page for the concert app

    :param request: Request from user
    :returns: Rendered front-page
    :rtype: HttpResponse
    """
    context = {'organiser': group_access(request.user, GROUP_ID['organiser']) or request.user.is_superuser}
    return render(request, 'concert/splash.html', context)


def techs(request):
    """ Renders page for technicians.

    :param request: HTTP-request, handled by Django
    :returns: Rendered web-page as HTTPResponse.
    :rtype: HttpResponse
    """
    user = request.user
    print("User: ", user)
    print("User ID: ", user.id)
    if not group_access(user, GROUP_ID['organiser']) and not user.is_superuser:
            return HttpResponse(False)

    if user.is_superuser:
        concert_list = Concert.objects.all()
    else:
        concert_list = Concert.objects.filter(organiser=user.id)

    employments = []
    for concert_list in concert_list:
        for tech in concert_list.techs.all():
            employments.append(dict(concert=concert_list.name[:32], stage=concert_list.stage.name[:32], tech=tech,
                                    task=Employment.objects.get(concert=concert_list, user=tech), time=concert_list.time))

    template = loader.get_template('concert/my_technicians.html')
    context = {'employments': employments}

    return HttpResponse(template.render(context, request))


@allow_access([GROUP_ID['booker'], GROUP_ID['organiser'], GROUP_ID['technician']])
def concerts(request):
    """Generates list of concerts the user is responsible for/at.

    :param request: Request from client
    :returns: HTTPResponse with rendered my_concerts.html"""

    user = request.user

    tpl = 'concert/my_concerts.html'

    concert_list = []

    if user.is_superuser or group_access(user, GROUP_ID['booker']):
        concert_list = Concert.objects.all()

    elif group_access(user, GROUP_ID['organiser']):
        # TODO: Fix hard-coded year 2017
        concert_list = Concert.objects.filter(time__year=2017)

    elif group_access(user, GROUP_ID['manager']):
        concert_list = Concert.objects.all().filter(band__manager_id=user.id)

    elif group_access(user, GROUP_ID['technician']):
        for employment in Employment.objects.filter(user=user.id):
            concert_list.append(dict(concert=employment.concert, stage=employment.concert.stage, task=employment.task,
                                     time=employment.concert.time, needs=employment.concert.needs))
        tpl = 'concert/my_employments.html'

    template = loader.get_template(tpl)
    context = {'concerts': concert_list}

    return HttpResponse(template.render(context, request))


@allow_access([GROUP_ID['manager']])
def manager(request):
    """Generates HTML for managers

    :param request: HTTP Request (given by Django)
    :rtype: HttpResponse
    :returns: HTTPResponse rendered with concert/manager.html"""

    user = request.user

    userType = GROUP_ID['manager']
    concert_list = []
    for concert in Concert.objects.filter(band__manager_id=user.id):
        editLink = "/concert/manager/edit/" + str(concert.id)
        concert_list.append(dict(concert=concert.name, stage=concert.stage, time=concert.time,
                                band=concert.band, needs=concert.needs, link=editLink))
    tpl = 'concert/manager.html'
    context = {'concerts': concert_list, 'userType': userType}

    template = loader.get_template(tpl)

    return HttpResponse(template.render(context, request))


def managerEdit(request, concertId):
    """Generates form to change concert needs.

    :param request:
    :param concertId: Id of concert
    :return: HTTP response with form rendered
    """

    form = concertNeedsForm.needsForm()
    concert = get_object_or_404(Concert, pk=concertId)
    context = {'concert': concert, 'form': form}
    tpl = loader.get_template('concert/manager_edit.html')

    return HttpResponse(tpl.render(context, request))


def updateConcertNeeds(request):
    """Handles submission of manager_edit.html (changes concert-needs)

    :param request: POST-request from form
    :return: HttpResponseRedirect to manager-site
    """
    if request.method == 'POST':
        form = concertNeedsForm.needsForm(request.POST)
        concertId = request.POST.get('concertId', None)
        print(concertId)
        if form.is_valid():
            try:
                concert = Concert.objects.get(id=concertId)
                print("Concert name: ", concert.name)
                concert.needs = form.cleaned_data['newNeeds']
                concert.save()
            except Concert.DoesNotExist:
                return HttpResponse("Failed to find concert with id" + str(concertId))

            return HttpResponseRedirect('/concert/manager')
        else:
            return HttpResponse("Form input was invalid")
    else:
        return HttpResponse("Oh dear, our devs have been silly")
