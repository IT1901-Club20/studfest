"""studfest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from frontpage import views

app_name='frontpage'
urlpatterns = [
    url(r'^login', views.loginn ,name='login'),
    url(r'^logout', views.logoutt, name='logout'),
    url(r'^concert1', views.concert1, name='concert1'),
    url(r'^concert2', views.concert2, name='concert2'),
    url(r'^concert3', views.concert3, name='concert3'),
    url(r'^', views.index,name='index'),
]
