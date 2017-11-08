# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


# TODO: Add Docstring!!
class LoginTest(TestCase):
    """Runs unittest for logging in, with valid and invalid password"""

    def setUp(self):
        User.objects.create_user(username="testUser", password="testPassword")

    def testValidLogin(self):
        c = Client()
        response = c.post('/login/', {'username': 'testUser', 'password': 'testPassword'})
        self.assertEqual(response.status_code, 302)
        response = c.get('/logout/')
        self.assertEqual(response.status_code, 302)

    # Sjekker om feil login-info gir
    def testInvalidLogin(self):
        c = Client()
        response = c.post('/login/', {'username': 'notAUser', 'password': 'notAPassword'})
        self.assertEqual(response.status_code, 302)


class RedirectionTest(TestCase):
    def setUp(self):
        organiserGroup = Group.objects.create(name='Organiser')
        technicianGroup = Group.objects.create(name='Technician')
        managerGroup = Group.objects.create(name='Manager')
        bookerGroup = Group.objects.create(name='Booker')
        headBookerGroup = Group.objects.create(name='Head Booker')

        organiser = User.objects.create_user(username="organiser", password="testPassword")
        organiser.groups.add(organiserGroup)
        technician = User.objects.create_user(username='technician', password='testPassword')
        technician.groups.add(technicianGroup)
        manager = User.objects.create_user(username='manager', password='testPassword')
        manager.groups.add(managerGroup)
        booker = User.objects.create_user(username='booker', password='testPassword')
        booker.groups.add(bookerGroup)
        headBooker = User.objects.create_user(username='headBooker', password='testPassword')
        headBooker.groups.add(headBookerGroup)

        multiple1 = User.objects.create_user(username='multiple1', password='testPassword')
        multiple1.groups.add(organiserGroup)
        multiple1.groups.add(technicianGroup)

        multiple2 = User.objects.create_user(username='multiple2', password='testPassword')
        multiple2.groups.add(managerGroup)
        multiple2.groups.add(bookerGroup)

        super1 = User.objects.create_superuser(username='super1', password='testPassword', email='super1@example.com')

        super2 = User.objects.create_superuser(username='super2', password='testPassword', email='super2@example.com')
        super2.groups.add(managerGroup)

        super3 = User.objects.create_superuser(username='super3', password='testPassword', email='super3@example.com')
        super3.groups.add(organiserGroup)
        super3.groups.add(technicianGroup)

    def testOrganiser(self):
        c = Client()
        response = c.post('/login/', {'username': 'organiser', 'password': 'testPassword'}, follow=True)
        self.assertRedirects(response, '/organiser')
        c.get('/logout/')

    def testTechnician(self):
        c = Client()
        response = c.post('/login/', {'username': 'technician', 'password': 'testPassword'}, follow=True)
        self.assertRedirects(response, '/concert/technicians', status_code=302)
        c.get('/logout/')

    def testManager(self):
        c = Client()
        response = c.post('/login/', {'username': 'manager', 'password': 'testPassword'}, follow=True)
        self.assertRedirects(response, '/concert/manager')
        c.get('/logout/')

    def testMultiple1(self):
        c = Client()
        c.post('/login/', {'username': 'multiple1', 'password': 'testPassword'}, follow=True)
        response = c.get('/')
        self.assertRedirects(response, '/roles/')
        c.get('/logout/')

    def testSuperNoGroup(self):
        c = Client()
        response = c.post('/login/', {'username': 'super1', 'password': 'testPassword'}, follow=True)
        self.assertRedirects(response, '/roles/')
        c.get('/logout/')

# TODO: add tests for superusers, no user, multiple user. Check that HTML contains right element.