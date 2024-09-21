from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse
from django.core import mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from videoflixbknd.tokens import account_activation_token  # Correct import path
import json
from django.template.loader import get_template

from django.template import TemplateDoesNotExist


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')

    def test_login(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

class CustomLogoutTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

class ActivateAccountTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword', is_active=False)
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = account_activation_token.make_token(self.user)

    def test_activate_account(self):
        response = self.client.get(reverse('activate_account', args=[self.uid, self.token]))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)


class TemplateLoadingTest(TestCase):
    def test_account_activation_email_template_exists(self):
        try:
            template = get_template('registration/account_activation_email.html')
        except TemplateDoesNotExist:
            self.fail('Template registration/account_activation_email.html does not exist')
            
            
class ResendActivationLinkTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword', is_active=False)

    def test_resend_activation_link(self):
        data = {
            'email': self.user.email
        }
        response = self.client.post(reverse('resend_activation_link'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Activation link has been resent. Please check your email.')
        
        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Activate your account', mail.outbox[0].subject)