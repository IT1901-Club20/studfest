"""Handles login, logout and redirection between pages
Functions:
*index(user)
*login(user)
*logout(user)
"""
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib import auth, messages
from django.urls import reverse
from common.restrictions import GROUP_ID, group_access, allow_access
from common.dictLookup import get_item

# Create your views here.
def getRoles(user):
    userGroups = []
    for group in user.groups.all():
        userGroups.append(group.id)
    return userGroups

def index(request):
    """Renders indexpage"""
    pages = {
        0: '/logout/',
        GROUP_ID['organiser']: "/",
        GROUP_ID['technician']: "concert/techs/",
        GROUP_ID['manager']: "concert/manager/",
        GROUP_ID['booker']: "/",
        GROUP_ID['head_booker']: "/"
    }
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect(reverse('frontpage:login'))

    userGroup = getRoles(user)
    print(userGroup)
    if len(userGroup) > 1:
        return HttpResponseRedirect("/roles/")
    else:
        return HttpResponseRedirect(pages[userGroup[0]])


    template = loader.get_template('frontpage/splash.html')
    context = {'organiser': group_access(request.user, GROUP_ID['organiser']) or request.user.is_superuser}
    return HttpResponse(template.render(context, request))


def multipleRoles(request):
    template = loader.get_template("frontpage/multipleRoles.html")
    user = request.user
    groups = getRoles(user)
    context = {
        'GROUP_ID': GROUP_ID,
        'roles': groups,
        'username': "Atle"
    }
    return HttpResponse(template.render(context, request))


def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            messages.error(request, "Incorrect username or password")
        return HttpResponseRedirect(reverse('frontpage:index',))
    if(request.user.is_authenticated):
        return HttpResponseRedirect(reverse('frontpage:index',))
    return render(request, 'frontpage/login.html', {})


def logout(request):
    if(request.user.is_authenticated):
        auth.logout(request)
        return HttpResponseRedirect(reverse('frontpage:login',))
    return render(request, 'frontpage/login.html', {})