# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models

# Create your models here.

class Manager(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

class Band(models.Model):
    name = models.CharField(max_length=200)
    manager = models.ForeignKey(Manager)

class Concert(models.Model):
    name = models.CharField(max_length=200)
    band = models.ForeignKey(Band)
    time = models.DateTimeField('Tidspunkt')

class Stage(models.Model):
    name = models.CharField(max_length=200)
