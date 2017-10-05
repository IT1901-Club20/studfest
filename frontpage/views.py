# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('frontpage:login',))
    return render(request, 'index.html', {})

def loginn(request):
    if(request.method=='POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
        return HttpResponseRedirect(reverse('frontpage:index',))
    if(request.user.is_authenticated):
        return HttpResponseRedirect(reverse('frontpage:index',))
    return render(request, 'login.html', {})

def logoutt(request):
    if(request.user.is_authenticated):
        logout(request)
        return HttpResponseRedirect(reverse('frontpage:login',))
    return render(request, 'login.html', {})

def concert1(request):
    if request.user.is_authenticated:
        return render(request, 'concert1.html', {'user':request.user.username})
    return HttpResponseRedirect(reverse('frontpage:login',))

def concert2(request):
    if request.user.is_authenticated:
        return render(request, 'concert2.html', {'user':request.user.username})
    return HttpResponseRedirect(reverse('frontpage:login',))

def concert3(request):
    if request.user.is_authenticated:
        return render(request, 'concert3.html', {'user':request.user.username})
    return HttpResponseRedirect(reverse('frontpage:login',))
