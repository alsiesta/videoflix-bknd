from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User, Group
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.tokens import default_token_generator  # Import the token generator


class UserViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_user_retrieval(self):
        response = self.client.get(reverse('user-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_user_creation(self):
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com'
        }
        response = self.client.post(reverse('user-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')

    def test_user_update(self):
        data = {
            'username': 'updateduser'
        }
        response = self.client.patch(reverse('user-detail', args=[self.user.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'updateduser')

    def test_user_deletion(self):
        response = self.client.delete(reverse('user-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())
        
class GroupViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.group = Group.objects.create(name='testgroup')
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_group_retrieval(self):
        response = self.client.get(reverse('group-detail', args=[self.group.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'testgroup')

    def test_group_update(self):
        data = {
            'name': 'updatedgroup'
        }
        response = self.client.patch(reverse('group-detail', args=[self.group.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'updatedgroup')

class MailResetPasswordTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')

    def test_mail_reset_password(self):
        data = {
            'email': self.user.email
        }
        response = self.client.post(reverse('mail_reset_password'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Password reset email has been sent to", response.data['detail'])

class PasswordResetConfirmTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)

    def test_password_reset_confirm(self):
        data = {
            'new_password': 'newtestpassword',
            'confirm_password': 'newtestpassword'
        }
        response = self.client.post(reverse('password_reset_confirm', args=[self.uid, self.token]), data)
        print(response.data)  # Debugging output
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()  # Refresh the user instance to get the updated password
        self.assertTrue(self.user.check_password('newtestpassword'))
        
        
class UserResetPasswordTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_user_reset_password(self):
        data = {
            'email': self.user.email,
            'old_password': 'testpassword',
            'new_password': 'newtestpassword',
            'confirm_password': 'newtestpassword'
        }
        response = self.client.post(reverse('reset_password'), data)  # Use 'reset_password' here
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()  # Refresh the user instance to get the updated password
        self.assertTrue(self.user.check_password('newtestpassword'))
        
class RegisterTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register(self):
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')