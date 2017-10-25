from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^concerts?$', views.concerts, name='concerts'),
    url(r'^techs?$', views.techs, name='technicians'),
    url(r'^technicians?$', views.techs, name='technicians'),
    url(r'^manager?$', views.manager, name='manager'),
    url(r'^manager/edit/(?P<concertId>[0-9])', views.managerEdit, name='manager'),
    url(r'^manager/submit', views.updateConcertNeeds, name='manager')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
