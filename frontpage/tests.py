# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase, Client
from django.contrib.auth.models import User


class LoginTest(TestCase):

    def setUp(self):
        User.objects.create_user(username="testUser", password="testPassword")

    # Sjekker om en vanlig bruker blir redirected til index når de logger inn,
    # om de kan logge ut, og om en ugyldig bruker ikke får tilgang
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
        self.assertEqual(response.status_code, 200)
