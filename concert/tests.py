# -*- coding: utf-8 -*-
#All tests concerning concerts

from __future__ import unicode_literals

from django.test import TestCase
from .models import Concert, Employment, Stage
from .views import


# Create your tests here.

class ConcertTestCase(TestCase):
    #name, organiser, stage, time, techs, band, needs
    def setUp(self):
        Concert.objects.create(name="lion", band="",stage="")
        Concert.objects.create(name="cat", sound="meow")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Concert.objects.get(name="lion")
        cat = Concert.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')
