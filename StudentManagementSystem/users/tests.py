from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='securepassword',
            role='student'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('securepassword'))
        self.assertEqual(user.role, 'student')


class UserAPITest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(username='student1', password='password123')

        # Log in and get the token
        response = self.client.post("/api/auth/token/login/", {"username": "student1", "password": "password123"})
        self.assertEqual(response.status_code, 200)  # Ensure login is successful
        self.token = response.data['auth_token']  # Save the token

    def test_login(self):
        # Use the token for authentication
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.get("/restricted-data/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_access_restricted_data(self):
        # Use the token for authentication
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.get("/restricted-data/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)