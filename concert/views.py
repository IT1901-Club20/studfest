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
from .models import Concert, Employment, Stage
from common.restrictions import GROUP_ID, group_access, allow_access
from . import concertNeedsForm


def index(request):
    template = loader.get_template('concert/splash.html')
    context = {'organiser': group_access(request.user, GROUP_ID['organiser']) or request.user.is_superuser}
    return HttpResponse(template.render(context, request))

@allow_access([GROUP_ID['organiser']])
def techs(request):
    """ Renders list of technicians for organiser.

    :param request: HTTP-request, handled by Django
    :return: Rendered webpage as HTTPResponse.
    :rtype: HttpResponse
    """

    user = request.user

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


@allow_access([GROUP_ID['booker'], GROUP_ID['organiser'], GROUP_ID['technician'], GROUP_ID['manager']])
def concerts(request):
    """Generates list of concerts the user is responsible for/at.

    Also filters the objects if specified in the GET-request
    :param request: Request from client
    :returns: HTTPResponse with rendered my_concerts.html"""

    user = request.user
    stage_filter = request.GET.get('stage_filter', '')
    tpl = 'concert/my_concerts.html'

    concert_list = []

    # TODO: Change name of function group_access.
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

    concert_list = filter(lambda concert: concert.stage.name == stage_filter or stage_filter == '', concert_list)
    template = loader.get_template(tpl)
    stages = Stage.objects.all()
    context = {
        'concerts': concert_list,
        'stages': stages,
        'stage_filter': stage_filter,
    }

    return HttpResponse(template.render(context, request))


@allow_access([GROUP_ID['manager']])
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


@allow_access([GROUP_ID['technician']])
def employments(request):
    """

    :param request:
    :return:
    """
    user = request.user

    concertList = Concert.objects.filter(techs__in= [user])
    jobs = []
    for c in concertList:
        jobs.append(c)

    print(concertList)
    print(jobs)

    context = {'concerts': jobs}
    template = loader.get_template("concert/my_employments.html")
    return HttpResponse(template.render(context, request))
