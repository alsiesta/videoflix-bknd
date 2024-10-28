# user/tests/test_signals.py

import logging
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)

class UserSignalTest(TestCase):
    def test_user_inactive_on_creation(self):
        logger.info("Creating new user")
        user = User.objects.create_user(username='newuser', email='newuser@example.com', password='newpassword')
        user.refresh_from_db()  # Refresh the user instance from the database
        logger.info(f"User {user.username} is_active: {user.is_active}")
        self.assertFalse(user.is_active)