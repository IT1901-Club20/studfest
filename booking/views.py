from datetime import date, time, datetime
from django.utils.timezone import make_aware
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.views.generic.edit import CreateView
from django.views.generic import View, ListView
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from band.models import Band
from common.restrictions import GROUP_ID, allow_access_class
from concert.models import Stage
from booking.models import Offer
# Create your views here.

@allow_access_class([GROUP_ID['booker'], GROUP_ID['head_booker']])
class OfferList(ListView):
    model = Offer
    template_name = "booking/offer_list.html"

class OfferForm(forms.Form):
     name = forms.CharField()
     band = forms.ModelChoiceField(queryset=Band.objects.all())
     stage = forms.ModelChoiceField(queryset=Stage.objects.all())
     date = forms.DateField()
     time = forms.TimeField()
     monetary_offer = forms.IntegerField()

@allow_access_class([GROUP_ID['booker'], GROUP_ID['head_booker']])
class SendOffer(CreateView):
    model = Offer
    fields = ['name', 'band', 'stage', 'monetary_offer', 'time']
    template_name = "booking/send.html"

    def get_initial(self):
        initial = {} #super(SendOffer, self).get_initial().copy()

        if 'id' in self.kwargs:
            initial['band'] = str(self.kwargs['id'])

        return initial

    def get_form(self):
        if self.request.POST:
            return OfferForm(data=self.request.POST)

        if 'id' in self.kwargs:
            return OfferForm(self.get_initial())

        return OfferForm()

    def form_invalid(self, form, **kwargs):
        #context = self.get_context_data(**kwargs)
        context = {}
        context['form'] = form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        #super(SendOffer, self).post(request, args, kwargs)
        form = self.get_form()

        if not form.is_valid():
            return self.form_invalid(form)

        _time = request.POST['date'] + ' ' + request.POST['time']
        _kwargs = {
            'name': request.POST['name'],
            'band': Band.objects.get(pk=request.POST['band']),
            'stage': Stage.objects.get(pk=request.POST['stage']),
            'time': make_aware(datetime.strptime(_time, "%Y-%m-%d %H:%M:%S")),
            'booker': request.user,
            'monetary_offer': request.POST['monetary_offer']
        }

        o = Offer(**_kwargs)
        lst = o.check_collision()

        if lst == [[],[]]:
            o.save()
            return HttpResponseRedirect(self.get_success_url())

        context = {}
        context['form'] = form
        context['band_collisions'] = lst[0]
        context['stage_collisions'] = lst[1]

        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('index')

@allow_access_class(GROUP_ID['head_booker']])
class ConfirmOffer(CreateView):
    pass
