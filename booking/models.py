# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
from band.models import Band
from concert.models import Concert, Stage

# Create your models here.

class Offer(models.Model):
    name = models.CharField(max_length=200, null=True)
    band = models.ForeignKey(Band, on_delete=models.SET_NULL, null=True)
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True)
    time = models.DateTimeField('Time and date')

    booker = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.SET_NULL, null=True,
                               related_name='booker')
    monetary_offer = models.IntegerField()
    approved_by_head_booker = models.BooleanField(default=False)
    approved_by_manager = models.BooleanField(default=False)

    def check_collision(self,
                        duration=timedelta(hours=1),
                        buffer_before=timedelta(minutes=15),
                        buffer_after=timedelta(minutes=15)):
        """
        Checks to see if the stage or band is already booked for another
        concert or offer.

        :returns: Two lists of concerts and bookings, one for band and
        one for stage.
        :rtype: List

        """
        band_concerts = []
        for c in self.band.concert_set.all():
            if self.time <= c.time_end and \
            self.time + duration >= c.time:
                band_concerts.append(c)

        stage_concerts = []
        for c in self.stage.concert_set.all():
            if self.time <= c.takedown_end and \
            self.time >= c.preparation_start:
                stage_concerts.append(c)

        return [band_concerts, stage_concerts]

    def create_concert(self):
        """
        Creates a concert object pased on the booking, if the offer is approved
        by head booker and manager.

        :returns: Nothing


        """
        if not (self.approved_by_head_booker and self.approved_by_manager):
            raise Exception("Skerpings!")

        #c = Concert(...)
        #c.save()
