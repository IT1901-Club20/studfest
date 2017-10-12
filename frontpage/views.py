# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.urls import reverse

# Create your views here.

ORGANISER_GROUP_ID = 1
TECHNICIAN_GROUP_ID = 2
MANAGER_GROUP_ID = 3


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('frontpage:login',))
    group = 0
    if len(request.user.groups.all()) > 0:
        if request.user.groups.all()[0].id == ORGANISER_GROUP_ID:
            #return HttpResponseRedirect(reverse('concert:index'))
            return HttpResponse("Har du ei gruppe? " + str(group))
    return render(request, 'frontpage/index.html', {})


def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('frontpage:index', ))
    if request.user.is_authenticated:
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
