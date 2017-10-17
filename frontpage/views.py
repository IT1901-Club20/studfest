# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib import auth, messages
from django.urls import reverse

# Create your views here.

ORGANISER_GROUP_ID = 1
TECHNICIAN_GROUP_ID = 2
MANAGER_GROUP_ID = 3

def group_access(user, *groups):
    for g in user.groups.all():
        if g.id in groups:
            return True

    return False

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('frontpage:login',))
    if not group_access(request.user, ORGANISER_GROUP_ID, TECHNICIAN_GROUP_ID):
            return HttpResponse(request.user.username + ", du har dessverre ikkje lov til å gå inn hit. #sorrynotsorry")
    template = loader.get_template('frontpage/splash.html')
    context = {'organiser': group_access(request.user, ORGANISER_GROUP_ID) or request.user.is_superuser}
    return HttpResponse(template.render(context, request))


def login(request):
    if(request.method=='POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
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

'''
def concert1(request):
    if request.user.is_authenticated:
        return render(request, 'frontpage/concert1.html', {'user':request.user.username})
    return HttpResponseRedirect(reverse('frontpage:login',))


def concert2(request):
    if request.user.is_authenticated:
        return render(request, 'frontpage/concert2.html', {'user':request.user.username})
    return HttpResponseRedirect(reverse('frontpage:login',))


def concert3(request):
    if request.user.is_authenticated:
        return render(request, 'frontpage/concert3.html', {'user':request.user.username})
    return HttpResponseRedirect(reverse('frontpage:login',))
'''
