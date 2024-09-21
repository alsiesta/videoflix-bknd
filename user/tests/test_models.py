from django.test import TestCase
from django.contrib.auth.models import User

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.check_password('testpassword'))

    def test_user_update(self):
        self.user.username = 'updateduser'
        self.user.save()
        self.assertEqual(self.user.username, 'updateduser')

    def test_user_deletion(self):
        user_id = self.user.id
        self.user.delete()
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=user_id)