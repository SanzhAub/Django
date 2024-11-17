from rest_framework import status
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
#from attendance.models import Attendance, Course, Student
from rest_framework.test import APIClient
from courses.models import Course, Enrollment
from students.models import Student
from datetime import date
from rest_framework import status

class AttendancePermissionsTest(TestCase):
    def setUp(self):
        User = get_user_model()

        self.student_user = User.objects.create_user(username="student", password="password123", role="student")
        self.teacher_user = User.objects.create_user(username="teacher", password="password123", role="teacher")
        
        self.student = Student.objects.create(user=self.student_user)
        self.teacher = Student.objects.create(user=self.teacher_user)

        self.course = Course.objects.create(name="Math 101")
 
        self.enrollment = Enrollment.objects.create(course=self.course, student=self.student)

        self.client = APIClient()

        self.student_token = Token.objects.create(user=self.student_user)
        self.teacher_token = Token.objects.create(user=self.teacher_user)

    def test_teacher_can_mark_attendance(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.teacher_token.key}")

        data = {
            "student": self.student.id,
            "course": self.course.id,  
            "date": date.today()  
        }

        
        response = self.client.post(f"/attendance/mark/{self.course.id}/", data)  

        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_cannot_mark_attendance(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.student_token.key}")

        data = {
            "student": self.student.id,
            "course": self.course.id,  
            "date": date.today()  
        }
        
        response = self.client.post(f"/attendance/mark/{self.course.id}/", data)  

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
