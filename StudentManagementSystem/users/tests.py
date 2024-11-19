from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
from users.serializers import UserSerializer
from users.permissions import IsStudent, IsTeacher, IsAdmin


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='testuser', password='password123', email='test@example.com', role='student')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.role, 'student')
        self.assertTrue(user.check_password('password123'))


class UserSerializerTest(TestCase):
    def test_user_serializer(self):
        user = User.objects.create_user(username='testuser', password='password123', email='test@example.com', role='student')
        serializer = UserSerializer(user)
        data = serializer.data
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['role'], 'student')


class UserPermissionTest(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(username='student', password='password', role='student')
        self.teacher = User.objects.create_user(username='teacher', password='password', role='teacher')
        self.admin = User.objects.create_user(username='admin', password='password', role='admin')

    def test_is_student_permission(self):
        self.client.login(username='student', password='password')
        request = self.client.get('/restricted-data/')  # Example endpoint
        self.assertTrue(IsStudent().has_permission(request.wsgi_request, None))

    def test_is_teacher_permission(self):
        self.client.login(username='teacher', password='password')
        request = self.client.get('/restricted-data/')
        self.assertTrue(IsTeacher().has_permission(request.wsgi_request, None))

    def test_is_admin_permission(self):
        self.client.login(username='admin', password='password')
        request = self.client.get('/restricted-data/')
        self.assertTrue(IsAdmin().has_permission(request.wsgi_request, None))


class UserViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.student = User.objects.create_user(username='student', password='password', role='student')
        self.teacher = User.objects.create_user(username='teacher', password='password', role='teacher')

    def test_user_registration(self):
        data = {
            "username": "testuser",
            "password": "Sanzh.aub2004",
            "email": "testuser@example.com",
            "role": "student"
        }
        response = self.client.post('/api/auth/users/', data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

def test_user_profile(self):
    self.client.force_authenticate(user=self.student)
    response = self.client.get('/users/profile/')
    self.assertEqual(response.status_code, status.HTTP_200_OK)

def test_restricted_data_access_denied(self):
    self.client.force_authenticate(user=self.student)
    response = self.client.get('/users/restricted-data/')
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

def test_restricted_data_access_granted(self):
    self.client.force_authenticate(user=self.teacher)
    response = self.client.get('/users/restricted-data/')
    self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_user_profile(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/users/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.student.username)

    def test_restricted_data_access_denied(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/users/restricted-data/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_restricted_data_access_granted(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get('/users/restricted-data/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'This is restricted data.')
