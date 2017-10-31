from django.shortcuts import render
from django.http import HttpResponse
from booking.models import Offer
from band.models import Band

# Create your views here.

def index(request):
    a=Offer(band=Band.objects.get(pk=2), time='2017-10-12 21:00:00')
    return HttpResponse(a.check_collision())
