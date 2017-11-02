from datetime import date, time, datetime
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.views.generic.edit import CreateView
from django.views.generic import View, ListView
from django.http import HttpResponse
from band.models import Band
from concert.models import Stage
from booking.models import Offer
# Create your views here.

class OfferList(ListView):
    model = Offer

class OfferForm(forms.Form):
     name = forms.CharField()
     band = forms.ModelChoiceField(queryset=Band.objects.all())
     stage = forms.ModelChoiceField(queryset=Stage.objects.all())
     date = forms.DateField()
     time = forms.TimeField()
     monetary_offer = forms.IntegerField()


class SendOffer(CreateView):
    model = Offer
    fields = ['name', 'band', 'stage', 'monetary_offer', 'time']
    template_name = "booking/send.html"

    def get_initial(self):
        initial = super(SendOffer, self).get_initial().copy()

        if 'id' in self.kwargs:
            initial['band'] = str(self.kwargs['id'])

        return initial


    def get_form(self):
        form = OfferForm
        return form

    def post(self, request, *args, **kwargs):
        _time = request.POST['date'] + ' ' + request.POST['time']
        _kwargs = {
            'name': request.POST['name'],
            'band': Band.objects.get(pk=request.POST['band']),
            'stage': Stage.objects.get(pk=request.POST['stage']),
            'time': datetime.strptime(_time, "%Y-%m-%d %H:%M:%S"),
            'booker': request.user,
            'monetary_offer': request.POST['monetary_offer']
        }

        html = ''
        for kw in Offer(**_kwargs).__dict__.items():
            html += '<p>' + str(kw) + '</p>\n'
        return HttpResponse(html)
