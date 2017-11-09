"""Studfests band-app
Renders html-pages of bands
Functions:
*index(request)
*detail(request, band_id)
"""

from django.shortcuts import render, get_object_or_404
from .models import Band
from common.restrictions import GROUP_ID, allow_access


@allow_access([GROUP_ID['head_booker'], GROUP_ID['booker'], GROUP_ID['organiser'], GROUP_ID['manager']])
def index(request):
    """Views all bands

    Shows the list of all bands
    :param request: Request from client
    :returns: HTTPResponse with band/index.html rendered with all bands as context
    """

    bands = Band.objects.all()
    context = {'bands': bands}
    return render(request, 'band/index.html', context)


@allow_access([GROUP_ID['head_booker'], GROUP_ID['booker'], GROUP_ID['organiser'], GROUP_ID['manager']])
def detail(request, band_id):
    """Views a single band

    Show info about a specific band, return a 404 if band not found
    :param request: Request from client
    :param band_id: The id of the band to be viewed
    :returns: HTTPResponse with band/detail.html rendered with the specific band as context
    """

    band = get_object_or_404(Band, pk=band_id)
    context = {'band': band}
    return render(request, 'band/detail.html', context)
