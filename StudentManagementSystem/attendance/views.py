from rest_framework import generics
from attendance.models import Attendance
from attendance.serializers import AttendanceSerializer
from rest_framework.permissions import IsAuthenticated
import logging
from courses.models import Course, Enrollment
from students.models import Student
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class AttendanceListCreateView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

logger = logging.getLogger('student_management')

class MarkAttendanceView(APIView):
    def post(self, request, course_id, student_id):
        try:
            course = Course.objects.get(id=course_id)
            student = Student.objects.get(id=student_id)
            attendance = Attendance.objects.create(student=student, course=course, status='present')
            logger.info(f"Attendance marked for student {student.name} in course {course.name}")
            return Response({"message": "Attendance marked"}, status=status.HTTP_200_OK)
        except Course.DoesNotExist or Student.DoesNotExist:
            return Response({"error": "Course or student not found"}, status=status.HTTP_404_NOT_FOUND)
