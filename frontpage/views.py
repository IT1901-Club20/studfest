""" Handles the first pages and the general pages of the app.
Also, organisers pages are here for now, as this role is yet to get it's own app.

Views have the following functions:
*multiple_roles(request)
*index(request)
*login(request)
*logout(request)
*organiser(request)

"""
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.urls import reverse
from common.restrictions import GROUP_ID, allow_access
# Create your views here.


@allow_access(GROUP_ID.values())
def multiple_roles(request):
    """Site for user with multiple roles. Link to different apps and features.
    The template, multiple_roles.html, uses strings identical to the keys in GROUP_ID
    to identify roles (i.e. {% if 'organiser' in roles %}). If these global variables changes,
    these must also change.

    :param request: GET-request from user
    :return: HttpResponse with rendered page
    """
    user = request.user
    roles = []
    for g in GROUP_ID.keys():
        if g in [group.id for group in user.groups.all()]:
            roles.append(g)

    context = {
        'username': user.username,
        'roles': roles
    }

    template = loader.get_template("frontpage/multiple_roles.html")
    return HttpResponse(template.render(context, request))


@allow_access(GROUP_ID.values())
def index(request):
    """Redirects to app based on role(s)
    If user has several roles, redirects to splash-like page.
    Else, chooses url from dict pages to redirect to.

    :rtype: HttpResponseRedirect
    :return: Redircetion to appropriate site"""

    user = request.user
    pages = {
        GROUP_ID['organiser']: "/organiser",
        GROUP_ID['technician']: "/concert/techicians",
        GROUP_ID['manager']: "/concert/manager",
        GROUP_ID['booker']: "/booker/",
        GROUP_ID['head_booker']: "/booker/"
    }
    roles = []
    for group in user.groups.all():
        if group.id in GROUP_ID.values():
            roles.append(group.id)

    if len(roles) > 1:
        return HttpResponseRedirect("/roles/")

    print(pages.keys())
    print(roles)

    return HttpResponseRedirect(pages[roles[0]])


def login(request):
    """Makes login-page. If user already is logged in, forwards to index, which in turn forwards to apropriate page
    If request is POST, authenticates user

    :param request: Request from client
    :return: rendered login-page
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            auth.login(request, user)
        return HttpResponseRedirect(reverse('frontpage:index',))
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('frontpage:index',))
    return render(request, 'frontpage/login.html', {})


def logout(request):
    """Signs user out

    :param request: GET-request from client
    :return: Rendered login-page
    """
    if request.user.is_authenticated:
        auth.logout(request)
        return HttpResponseRedirect(reverse('frontpage:login',))
    return render(request, 'frontpage/login.html', {})


@allow_access(GROUP_ID['organiser'])
def organiser(request):
    """Renders organiser page. Access is handled by decorator"""
    template = loader.get_template('frontpage/splash.html')
    context = {'organiser': True}

    return HttpResponse(template.render(context, request))
