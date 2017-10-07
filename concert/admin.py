# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Band, Concert, Stage

# Register your models here.
admin.site.register(Band)
admin.site.register(Concert)
admin.site.register(Stage)
