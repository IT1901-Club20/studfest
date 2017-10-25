# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from band.models import Band, Genre

# Create your models here.

'''
class Manager(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

class Band(models.Model):
    name = models.CharField(max_length=200)
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
'''


class Stage(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, null=True)
    notes = models.CharField(max_length=2048, null=True)

    def __str__(self):
        return self.name


class Concert(models.Model):
    name = models.CharField(max_length=200)
    organiser = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.SET_NULL, null=True,
                                  related_name='organiser')
    band = models.ForeignKey(Band, on_delete=models.SET_NULL, null=True)
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True)
    techs = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   through='Employment', related_name='technicians')
    time = models.DateTimeField('Time and date')
    needs = models.CharField(max_length=2048, null=True)

    def __str__(self):
        return self.name


class Employment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)
    task = models.CharField(max_length=200)
    notes = models.CharField(max_length=2048)
