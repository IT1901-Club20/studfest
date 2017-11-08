from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^offer/send/(?P<id>[0-9]+)$', views.SendOffer.as_view(),
        name='send'),
    url(r'^offer/send/$', views.SendOffer.as_view(), name='send'),
    url(r'^offers$', views.OfferList.as_view(), name='index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
