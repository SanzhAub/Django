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
    permission_classes = [IsAuthenticated]
    
    def post(self, request, course_id):
        user = request.user

        # Only teachers can mark attendance
        if user.role != "teacher":
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        # Check course exists
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        # Mark attendance
        student_id = request.data.get("student_id")
        present = request.data.get("present", False)

        attendance = Attendance.objects.create(
            student_id=student_id, course=course, present=present
        )
        return Response({"detail": "Attendance marked successfully"}, status=status.HTTP_201_CREATED)
