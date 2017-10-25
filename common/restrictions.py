# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.template import loader

GROUP_ID = {
    'organiser': 1,
    'technician': 2,
    'manager': 3,
    'booker': 4,
    'head_booker': 5,
    }

def Http403(request):
    template = loader.get_template('403.html')
    context = {'front': request.scheme + '://' + request.get_host() + '/'}
    context['back'] =  request.META.get('HTTP_REFERER', context['front'])

    return HttpResponse(template.render(context, request))

def group_access(user, *groups):
    for g in groups:
        if g in [group.id for group in user.groups.all()]:
            return True
    return False

def owns_object(user, pk):
    return user.id is pk

def restrict_access(lst=[], pk=False):
    def call_func(func):
        def actual_decorator(request, *args, **kwargs):
            if request.user.is_superuser:
                return func(request, *args, **kwargs)
            if not group_access(request.user, *lst):
                if pk:
                    if owns_object(request.user, kwargs['pk']):
                        return func(request, *args, **kwargs)
                return Http403(request)
            return func(request, *args, **kwargs)

        return actual_decorator

    return call_func

def restrict_access_class(*args, **kwargs):
    return method_decorator(restrict_access(*args, **kwargs), name='dispatch')
