# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Concert, Stage, Employment

# Register your models here.
admin.site.register(Concert)
admin.site.register(Stage)
admin.site.register(Employment)
