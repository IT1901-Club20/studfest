from django.shortcuts import render, get_object_or_404
from .models import Band, Genre


def index(request):
    bands = Band.objects.all()
    context = {'bands': bands}
    return render(request, 'band/index.html', context)


def detail(request, band_id):
    band = get_object_or_404(Band, pk=band_id)
    context = {'band': band}
    return render(request, 'band/detail.html', context)