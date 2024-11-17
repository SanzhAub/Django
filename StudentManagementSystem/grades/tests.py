from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from courses.models import Course

class GradeAPITest(APITestCase):
    def setUp(self):
        self.teacher = get_user_model().objects.create_user(username='teacher1', password='password123', role='teacher')
        self.student = get_user_model().objects.create_user(username='student1', password='password123', role='student')
        self.course = Course.objects.create(name="Math 101")
        response = self.client.post("/api/auth/token/login/", {"username": "teacher1", "password": "password123"})
        self.token = response.data['auth_token']

    def test_add_grade(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        data = {
            "student": self.student.id,
            "course": self.course.id,
            "grade": "A",
            "teacher": self.teacher.id,
        }
        response = self.client.post("/grades/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

