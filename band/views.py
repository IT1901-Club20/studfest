from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Band, Genre


def index(request):
    template = loader.get_template('band/index.html')
    bands = Band.objects.all()
    context = {
        'bands': bands,
    }
    return HttpResponse(template.render(context, request))
