# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


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

    def testConcertAccessNotLoggedIn(self):
        c = Client()
        response = c.get('/concert/')
        self.assertEqual(response.status_code, 302)

    def testConcertAccessOrganiser(self):
        c = Client()
        c.post('/login/', {'username': 'organiser', 'password': 'testPassword'})
        response = c.get('/concert/')
        self.assertEqual(response.status_code, 200)

    def testConcertAccessTechnician(self):
        c = Client()
        c.post('/login/', {'username': 'technician', 'password': 'testPassword'})
        response = c.get('/concert/')
        self.assertEqual(response.status_code, 200)

    def testConcertAccessManager(self):
        c = Client()
        c.post('/login/', {'username': 'manager', 'password': 'testPassword'})
        response = c.get('/concert/')
        self.assertEqual(response.status_code, 200)

    def testConcertAccessBooker(self):
        c = Client()
        c.post('/login/', {'username': 'booker', 'password': 'testPassword'})
        response = c.get('/concert/')
        self.assertEqual(response.status_code, 200)

    def testConcertAccessHeadBooker(self):
        c = Client()
        c.post('/login/', {'username': 'head_booker', 'password': 'testPassword'})
        response = c.get('/concert/')
        self.assertEqual(response.status_code, 200)

    def testTechniciansAccessNotLoggedIn(self):
        c = Client()
        response = c.get('/concert/technician')
        self.assertEqual(response.status_code, 302)

    def testTechniciansAccessOrganiser(self):
        c = Client()
        c.post('/login/', {'username': 'organiser', 'password': 'testPassword'})
        response = c.get('/concert/technician')
        self.assertEqual(response.status_code, 200)

    def testTechniciansAccessTechnician(self):
        c = Client()
        c.post('/login/', {'username': 'technician', 'password': 'testPassword'})
        response = c.get('/concert/technician')
        self.assertEqual(response.status_code, 403)

    def testTechniciansAccessManager(self):
        c = Client()
        c.post('/login/', {'username': 'manager', 'password': 'testPassword'})
        response = c.get('/concert/technician')
        self.assertEqual(response.status_code, 403)

    def testTechniciansAccessBooker(self):
        c = Client()
        c.post('/login/', {'username': 'booker', 'password': 'testPassword'})
        response = c.get('/concert/technician')
        self.assertEqual(response.status_code, 403)

    def testTechniciansAccessHeadBooker(self):
        c = Client()
        c.post('/login/', {'username': 'head_booker', 'password': 'testPassword'})
        response = c.get('/concert/technician')
        self.assertEqual(response.status_code, 403)

    def testConcertConcertsAccessNotLoggedIn(self):
        c = Client()
        response = c.get('/concert/concerts')
        self.assertEqual(response.status_code, 302)

    def testConcertConcertsAccessOrganiser(self):
        c = Client()
        c.post('/login/', {'username': 'organiser', 'password': 'testPassword'})
        response = c.get('/concert/concerts')
        self.assertEqual(response.status_code, 200)

    def testConcertConcertsAccessTechnician(self):
        c = Client()
        c.post('/login/', {'username': 'technician', 'password': 'testPassword'})
        response = c.get('/concert/concerts')
        self.assertEqual(response.status_code, 200)

    def testConcertConcertsAccessManager(self):
        c = Client()
        c.post('/login/', {'username': 'manager', 'password': 'testPassword'})
        response = c.get('/concert/concerts')
        self.assertEqual(response.status_code, 200)

    def testConcertConcertsAccessBooker(self):
        c = Client()
        c.post('/login/', {'username': 'booker', 'password': 'testPassword'})
        response = c.get('/concert/concerts')
        self.assertEqual(response.status_code, 200)

    def testConcertConcertsAccessHeadBooker(self):
        c = Client()
        c.post('/login/', {'username': 'head_booker', 'password': 'testPassword'})
        response = c.get('/concert/concerts')
        self.assertEqual(response.status_code, 200)
