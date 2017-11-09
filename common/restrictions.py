# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.exceptions import PermissionDenied

try:
    GROUP_ID = {
        'organiser': Group.objects.get(name__iexact="Organiser").id,
        'technician': Group.objects.get(name__iexact="Technician").id,
        'manager': Group.objects.get(name__iexact="Manager").id,
        'booker': Group.objects.get(name__iexact="Booker").id,
        'head_booker': Group.objects.get(name__iexact="Head booker").id,
    }
except:
    GROUP_ID = {
        'organiser': 1,
        'technician': 2,
        'manager': 3,
        'booker': 4,
        'head_booker': 5,
    }

# Er overflødig atm
def Http403(request):
    """
    Function to return a 403 page.

    :param request: HttpRequest
    :returns: A fitting 403 page
    :rtype: HttpResponse

    """
    template = loader.get_template('403.html')
    context = {'front': request.scheme + '://' + request.get_host() + '/'}
    context['back'] =  request.META.get('HTTP_REFERER', context['front'])

    return HttpResponse(template.render(context, request))


def group_access(user, *groups, ret=bool):
    """
    Iterates the groups of which a user is a member, and checks if at
    least on if them is listed in

    :param User user: Object for the logged in user
    :param list groups: List of allowed groups
    :param function ret: Function to wrap the rtype
    :rtype: bool (unless defined otherwise in "ret"
    :returns: Value for whether or not user belongs allowed group
    """

    for g in groups:
        if g in [group.id for group in user.groups.all()]:
            return ret(g)
    return ret(0)


def owns_object(user, pk):
    """
    Compares the user's id with the primary key, to see if the user
    "owns" the object being requested.

    :param user: Object for logged in user
    :param pk: Primary key from the get request
    :returns: Whether user.id matches pk
    :rtype: bool

    """
    return user.id is pk


def allow_access(lst=[], pk=False):
    """
    Returns the called if the user is allowed to access it; a 403 page
    if not.

    :param lst: ID numbers for the allowed classes
    :param pk: Whether or not the class access can be overridden if the
               user "owns" the object
    :returns: Called function
    :rtype:
    """

    def call_func(func):
        def actual_decorator(request, *args, **kwargs):
            if not request.user.is_authenticated():
                return HttpResponseRedirect("/login/")
            if request.user.is_superuser:
                return func(request, *args, **kwargs)
            if not group_access(request.user, *lst):
                if pk:
                    if owns_object(request.user, kwargs['pk']):
                        return func(request, *args, **kwargs)
                raise PermissionDenied

            return func(request, *args, **kwargs)

        return actual_decorator

    return call_func


def allow_access_class(*args, **kwargs):
    """
    Decorates the dispatch method of a view class with "allow_access".

    :returns: View class
    :rtype: View

    """
    return method_decorator(allow_access(*args, **kwargs), name='dispatch')
