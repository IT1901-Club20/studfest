# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Band


class AccessTest(TestCase):
    def setUp(self):
        organiser_group = Group.objects.create(name='Organiser')
        technician_group = Group.objects.create(name='Technician')
        manager_group = Group.objects.create(name='Manager')
        booker_group = Group.objects.create(name='Booker')
        head_booker_group = Group.objects.create(name='Head Booker')

        organiser = User.objects.create_user(username="organiser", password="testPassword")
        organiser.groups.add(organiser_group)
        technician = User.objects.create_user(username='technician', password='testPassword')
        technician.groups.add(technician_group)
        manager = User.objects.create_user(username='manager', password='testPassword')
        manager.groups.add(manager_group)
        booker = User.objects.create_user(username='booker', password='testPassword')
        booker.groups.add(booker_group)
        head_booker = User.objects.create_user(username='head_booker', password='testPassword')
        head_booker.groups.add(head_booker_group)

        Band.objects.create(pk=1, name='test_band')

    def testBandAccessNotLoggedIn(self):
        c = Client()
        response = c.get('/band/')
        self.assertEqual(response.status_code, 403)

    def testBandAccessOrganiser(self):
        c = Client()
        c.post('/login/', {'username': 'organiser', 'password': 'testPassword'})
        response = c.get('/band/')
        self.assertEqual(response.status_code, 200)

    def testBandAccessTechnician(self):
        c = Client()
        c.post('/login/', {'username': 'technician', 'password': 'testPassword'})
        response = c.get('/band/')
        self.assertEqual(response.status_code, 403)

    def testBandAccessManager(self):
        c = Client()
        c.post('/login/', {'username': 'manager', 'password': 'testPassword'})
        response = c.get('/band/')
        self.assertEqual(response.status_code, 200)

    def testBandAccessBooker(self):
        c = Client()
        c.post('/login/', {'username': 'booker', 'password': 'testPassword'})
        response = c.get('/band/')
        self.assertEqual(response.status_code, 200)

    def testBandAccessHeadBooker(self):
        c = Client()
        c.post('/login/', {'username': 'head_booker', 'password': 'testPassword'})
        response = c.get('/band/')
        self.assertEqual(response.status_code, 200)

    def testBandDetailAccessNotLoggedIn(self):
        c = Client()
        response = c.get('/band/1/')
        self.assertEqual(response.status_code, 403)

    def testBandDetailAccessOrganiser(self):
        c = Client()
        c.post('/login/', {'username': 'organiser', 'password': 'testPassword'})
        response = c.get('/band/1/')
        self.assertEqual(response.status_code, 200)

    def testBandDetailAccessTechnician(self):
        c = Client()
        c.post('/login/', {'username': 'technician', 'password': 'testPassword'})
        response = c.get('/band/1/')
        self.assertEqual(response.status_code, 403)

    def testBandDetailAccessManager(self):
        c = Client()
        c.post('/login/', {'username': 'manager', 'password': 'testPassword'})
        response = c.get('/band/1/')
        self.assertEqual(response.status_code, 200)

    def testBandDetailAccessBooker(self):
        c = Client()
        c.post('/login/', {'username': 'booker', 'password': 'testPassword'})
        response = c.get('/band/1/')
        self.assertEqual(response.status_code, 200)

    def testBandDetailAccessHeadBooker(self):
        c = Client()
        c.post('/login/', {'username': 'head_booker', 'password': 'testPassword'})
        response = c.get('/band/1/')
        self.assertEqual(response.status_code, 200)

    def testNoBandReturns404(self):
        c = Client()
        c.post('/login/', {'username': 'head_booker', 'password': 'testPassword'})
        response = c.get('/band/2/')
        self.assertEqual(response.status_code, 404)
