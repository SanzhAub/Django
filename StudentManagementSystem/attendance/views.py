from rest_framework import generics, status
from attendance.models import Attendance
from attendance.serializers import AttendanceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from courses.models import Course, Enrollment
from students.models import Student
import logging

logger = logging.getLogger('student_management')

class AttendanceListCreateView(generics.ListCreateAPIView):

    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]


class MarkAttendanceView(APIView):
   
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        user = request.user

        if user.role != "teacher":
            logger.warning(f"Unauthorized access attempt by user {user.username}")
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            logger.error(f"Course with ID {course_id} not found.")
            return Response({"detail": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        student_id = request.data.get("student_id")
        if not student_id:
            return Response({"detail": "Student ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            logger.error(f"Student with ID {student_id} not found.")
            return Response({"detail": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        if not Enrollment.objects.filter(student=student, course=course).exists():
            logger.warning(f"Student {student.id} is not enrolled in course {course.id}.")
            return Response({"detail": "Student is not enrolled in this course"}, status=status.HTTP_400_BAD_REQUEST)

        present = request.data.get("present")
        if present not in [True, False]:
            return Response({"detail": "Invalid value for 'present' (must be True or False)"}, status=status.HTTP_400_BAD_REQUEST)

        attendance = Attendance.objects.create(
            student=student, course=course, status="present" if present else "absent"
        )

        logger.info(f"Attendance marked for student {student.id} ({student.username}) in course {course.id} ({course.name}).")
        return Response(
            {
                "detail": "Attendance marked successfully",
                "student": student.username,
                "course": course.name,
                "status": "present" if present else "absent"
            },
            status=status.HTTP_201_CREATED
        )
