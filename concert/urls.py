from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^techs?$', views.techs, name='technicians'),
    url(r'^technicians?$', views.techs, name='technicians'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
