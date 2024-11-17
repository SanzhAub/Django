from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

class GradeAPITest(APITestCase):
    def setUp(self):
        self.teacher = get_user_model().objects.create_user(username='teacher1', password='password123', role='teacher')
        response = self.client.post("/api/auth/token/login/", {"username": "teacher1", "password": "password123"})
        self.token = response.data['auth_token']

    def test_add_grade(self):
        # Authenticate the user by setting the token in the headers
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        data = {
            "student": 1,  # Assuming you have a student with ID 1
            "course": 1,   # Assuming you have a course with ID 1
            "grade": "A"
        }
        response = self.client.post("/grades/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)