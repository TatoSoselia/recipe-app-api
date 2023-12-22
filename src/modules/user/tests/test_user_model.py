"""Tests for user model."""

from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):
    """Test user model."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'test_pass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_with_normalized_email(self):
        """Test creating a user with normalized email is successful."""
        emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email in emails:
            user = get_user_model().objects.create_user(
                email=email[0],
                password='test_pass123',
            )
            self.assertEqual(user.email, email[1])
