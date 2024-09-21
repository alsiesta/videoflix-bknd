from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient
from user.serializers import GroupSerializer, RegistrationSerializer, EmailPasswordResetSerializer, UserSerializer
from django.contrib.auth.models import Group, User

class UserSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.factory = APIRequestFactory()

    def test_user_serializer(self):
        request = self.factory.get('/')
        serializer = UserSerializer(instance=self.user, context={'request': request})
        data = serializer.data
        self.assertEqual(data['username'], self.user.username)

class GroupSerializerTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name='Test Group')
        self.factory = APIRequestFactory()

    def test_group_serializer(self):
        request = self.factory.get('/')
        serializer = GroupSerializer(instance=self.group, context={'request': request})
        data = serializer.data
        self.assertEqual(data['name'], self.group.name)

class PasswordResetSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_password_reset_serializer(self):
        data = {
            'email': self.user.email,
            'old_password': 'testpassword',
            'new_password': 'newtestpassword',
            'confirm_password': 'newtestpassword'
        }
        response = self.client.post('/user/user_reset_password/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], "Password has been reset successfully.")

class EmailPasswordResetSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.factory = APIRequestFactory()

    def test_email_password_reset_serializer(self):
        request = self.factory.post('/')
        force_authenticate(request, user=self.user)
        data = {'email': self.user.email}
        serializer = EmailPasswordResetSerializer(data=data, context={'request': request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data['email'], self.user.email)
        
class NewPasswordResetSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_new_password_reset_serializer(self):
        data = {
            'email': self.user.email,
            'old_password': 'testpassword',
            'new_password': 'newtestpassword',
            'confirm_password': 'newtestpassword'
        }
        response = self.client.post('/user/user_reset_password/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], "Password has been reset successfully.")
        

class RegistrationSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_registration_serializer(self):
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com'
        }
        request = self.factory.post('/user/register/', data)
        serializer = RegistrationSerializer(data=data, context={'request': request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')