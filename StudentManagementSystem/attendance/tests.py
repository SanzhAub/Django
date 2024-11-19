from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from attendance.models import Attendance
from courses.models import Course, Enrollment
from students.models import Student
from rest_framework.authtoken.models import Token


User = get_user_model()

class AttendanceTests(APITestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(username='teacher', password='teacher123', role='teacher')
        self.student_user = User.objects.create_user(username='student', password='student123', role='student')

        self.student = Student.objects.create(user=self.student_user)

        self.course = Course.objects.create(name='Math 101', description='Basic Math Course')

        Enrollment.objects.create(student=self.student, course=self.course)
        print(Enrollment.objects.filter(student=self.student, course=self.course).exists())

        self.token = Token.objects.create(user=self.teacher)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_list_attendance(self):
        Attendance.objects.create(student=self.student, course=self.course, date="2024-11-01", status="present")

        response = self.client.get('/attendance/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'present')

    def test_mark_attendance(self):
        data = {
            "student_id": self.student.id,
            "present": True
        }
        response = self.client.post(
            reverse("mark-attendance", kwargs={"course_id": self.course.id}),
            data
            )

        print(f"Request data: {data}")
        print(f"Response: {response.status_code}, {response.data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'present')

        attendance = Attendance.objects.filter(student=self.student, course=self.course).first()
        self.assertIsNotNone(attendance)
        self.assertEqual(attendance.status, 'present')

    def test_mark_attendance_forbidden(self):
        self.client.login(username='student', password='student123')

        data = {
            "student_id": self.student.id,
            "present": True
        }
        response = self.client.post(f'/attendance/mark/{self.course.id}/', data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_mark_attendance_course_not_found(self):
        data = {
            "student_id": self.student.id,
            "present": True
        }
        response = self.client.post('/attendance/mark/9999/', data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_mark_attendance_student_not_enrolled(self):
        new_user = User.objects.create_user(username='new_student', password='newstudent123', role='student')
        new_student = Student.objects.create(user=new_user)

        data = {
            "student_id": new_student.id,
            "present": True
        }
        response = self.client.post(f'/attendance/mark/{self.course.id}/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Student is not enrolled in this course')

    def test_mark_attendance_invalid_present_value(self):
        self.client.login(username='student', password='password')
        data = {'student_id': self.student.id, 'present': 'invalid_value'}
        response = self.client.post(f'/attendance/mark/{self.course.id}/', data, format='json')
        
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "'present' must be a boolean value (True or False).")

    def test_mark_attendance_missing_student_id(self):
        data = {
            "present": True
        }
        response = self.client.post(f'/attendance/mark/{self.course.id}/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Student ID is required')
