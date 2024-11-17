from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

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



class UserAPITest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.student_user = User.objects.create_user(username="student", password="password123", role="student")
        self.teacher_user = User.objects.create_user(username="teacher", password="password123", role="teacher")
        
        self.client = APIClient()

        self.student_token = Token.objects.create(user=self.student_user)
        self.teacher_token = Token.objects.create(user=self.teacher_user)

    def test_login(self):
        response = self.client.post("/auth/token/login/", {
            "username": "student",
            "password": "password123"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['auth_token']

    def test_access_restricted_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.teacher_token.key}")
        response = self.client.get("/restricted-data/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.student_token.key}")
        response = self.client.get("/restricted-data/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_cannot_mark_attendance(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.student_token.key}")
        response = self.client.post("/attendance/mark/1/", {"course_id": 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_can_mark_attendance(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.teacher_token.key}")
        response = self.client.post("/attendance/mark/1/", {"course_id": 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
