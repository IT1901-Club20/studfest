"""Studfests concert-app

Renders html-pages based on user. Permission-restriction done through @restrict-access decorator.
Functions:
*Index(request)
*techs(request)
*concerts(request)
*manager(request)
"""
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Concert, Employment
from common.restrictions import GROUP_ID, group_access, restrict_access
from . import concertNeedsForm


def index(request):
    template = loader.get_template('concert/splash.html')
    context = {'organiser': group_access(request.user, GROUP_ID['organiser']) or request.user.is_superuser}
    return HttpResponse(template.render(context, request))


def techs(request):
    """ Renders page for technicians.

    :param request: HTTP-request, handled by Django
    :return: Rendered webpage as HTTPResponse.
    :rtype: HttpResponse
    """

    user = request.user
    print("User: ", user)
    print("User ID: ", user.id)
    if not group_access(user, GROUP_ID['organiser']) and not user.is_superuser:
            return HttpResponse(False)

    if user.is_superuser:
        concertList = Concert.objects.all()
    else:
        concertList = Concert.objects.filter(organiser=user.id)

    employments = []
    for concertList in concertList:
        for tech in concertList.techs.all():
            employments.append(dict(concert=concertList.name[:32], stage=concertList.stage.name[:32], tech=tech,
                                    task=Employment.objects.get(concert=concertList, user=tech), time=concertList.time))

    template = loader.get_template('concert/my_technicians.html')
    context = {'employments': employments}

    return HttpResponse(template.render(context, request))


@restrict_access([GROUP_ID['booker'], GROUP_ID['organiser'], GROUP_ID['technician']])
def concerts(request):
    """Generates list of concerts the user is responsible for/at.

    :param request: Request from client
    :returns: HTTPResponse with rendered my_concerts.html"""

    user = request.user

    tpl = 'concert/my_concerts.html'

    concertList = []

    #TODO: Change name of function group_access.
    if user.is_superuser or group_access(user, GROUP_ID['booker']):
        concertList = Concert.objects.all()

    elif group_access(user, GROUP_ID['organiser']):
        #TODO: Fix hard-coded year 2017
        concertList = Concert.objects.filter(time__year=2017)

    elif group_access(user, GROUP_ID['techician']):
        for employment in Employment.objects.filter(user=user.id):
            concertList.append(dict(concert=employment.concert, stage=employment.concert.stage, task=employment.task,
                                    time=employment.concert.time, needs=employment.concert.needs))
        tpl = 'concert/my_employments.html'

    template = loader.get_template(tpl)
    context = {'concerts': concertList}

    return HttpResponse(template.render(context, request))


@restrict_access([GROUP_ID['manager']])
def manager(request):
    """Generates HTML for managers

    :param request: HTTP Request (given by Django)
    :rtype: HttpResponse
    :returns: HTTPResponse rendered with concert/manager.html"""

    user = request.user

    userType = GROUP_ID['manager']
    concertList = []
    for concert in Concert.objects.filter(band__manager_id=user.id):
        editLink = "/concert/manager/edit/" + str(concert.id)
        concertList.append(dict(concert=concert.name, stage=concert.stage, time=concert.time,
                                band=concert.band, needs=concert.needs, link=editLink))
    tpl = 'concert/manager.html'
    context = {'concerts': concertList, 'userType': userType}

    template = loader.get_template(tpl)

    return HttpResponse(template.render(context, request))


def managerEdit(request, concertId):
    """Generates form to change concert needs.

    :param request:
    :param concertId: Id of concert
    :return: HTTP response with form rendered
    """

    form = concertNeedsForm.needsForm()

    try:
        concert = Concert.objects.get(pk=concertId)
    except Concert.DoesNotExist:
        #TODO: Add proper not-found response
        return HttpResponse("Concert not found")

    context = {'concert': concert, 'form': form}
    tpl = loader.get_template("concert/manager_edit.html")

    return HttpResponse(tpl.render(context, request))


def updateConcertNeeds(request):
    """Handles submission of manager_edit.html (changes concert-needs)

    :param request: POST-request from form
    :return: HttpResposeRedirect to manager-site
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
