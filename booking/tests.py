# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from band.models import Band
from booking.models import Offer
from concert.models import Concert, Stage

# Create your tests here.

class OfferSendTest(TestCase):
    def setUp(self):
        for i in range(1,4):
            User(username=str(i)).save()

        band = Band()
        stage = Stage()

        band.save()
        stage.save()

        concert_date = make_aware(datetime(
            year=2017,
            month=11,
            day=17,
            hour=20
        ))

        Concert(
            name="Veldig fredag",
            organiser=User.objects.get(pk=1),
            band=band,
            stage=stage,
            preparation_start=concert_date - timedelta(minutes=30),
            time=concert_date,
            time_end=concert_date + timedelta(hours=1),
            takedown_end=concert_date + timedelta(hours=1, minutes=30),
            needs="Ver flink!"
        ).save()

        Offer(
            name="Veldig Laurdag",
            band=band,
            stage=stage,
            time=concert_date,
            booker=User.objects.get(pk=2),
            monetary_offer=10
        ).save()

        Offer(
            name="Veldig Laurdag",
            band=band,
            stage=stage,
            time=concert_date + timedelta(days=1),
            booker=User.objects.get(pk=2),
            monetary_offer=10
        ).save()


    def test_invalid_offer(self):
        o = Offer.objects.get(pk=1)
        self.assertNotEqual(o.check_collision(), [[],[]])

    def test_valid_offer(self):
        o = Offer.objects.get(pk=2)
        print(o.time)
        self.assertEqual(o.check_collision(), [[],[]])

    def test_create_concert(self):
        o = Offer.objects.get(pk=2)
        o.approved_by_head_booker = True
        o.approved_by_manager = True
        o.create_concert()

        self.assertEqual(bool(Concert.objects.get(pk=2)), True)
