from django.test import TestCase
from users.models import User
from courses.models import Course
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

class AttendancePermissionsTest(APITestCase):
    def setUp(self):
        # Create users
        self.student = get_user_model().objects.create_user(username='student1', password='password123', role='student')
        self.teacher = get_user_model().objects.create_user(username='teacher1', password='password123', role='teacher')
        
        # Log in and get the token for each user
        student_response = self.client.post("/api/auth/token/login/", {"username": "student1", "password": "password123"})
        self.student_token = student_response.data['auth_token']

        teacher_response = self.client.post("/api/auth/token/login/", {"username": "teacher1", "password": "password123"})
        self.teacher_token = teacher_response.data['auth_token']

    def test_student_cannot_mark_attendance(self):
        # Authenticate as student
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.student_token}")
        response = self.client.post("/attendance/mark/1/")
        self.assertEqual(response.status_code, 403)  # Students cannot mark attendance

    def test_teacher_can_mark_attendance(self):
        # Authenticate as teacher
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.teacher_token}")
        response = self.client.post("/attendance/mark/1/")
        self.assertEqual(response.status_code, 201)  # Teachers can mark attendance
