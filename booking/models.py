# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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

    def check_collision():
        """
        Checks to see if the stage or band is already booked for another
        concert or offer.

        :returns: A list of the concerts and bookings, if any.
        :rtype: List

        """
        pass

    def create_concert():
        """
        Creates a concert object pased on the booking, if the offer is approved
        by head booker and manager.

        :returns: Nothing


        """
        if not (self.approved_by_head_booker and self.approved_by_manager):
            raise Exception("Skerpings!")

        #c = Concert(...)
        #c.save()
