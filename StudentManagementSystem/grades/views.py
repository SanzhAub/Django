from rest_framework import generics
from grades.models import Grade
from grades.serializers import GradeSerializer
from rest_framework.permissions import IsAuthenticated
import logging
from courses.models import Course
from students.models import Student
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class GradeListCreateView(generics.ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]

logger = logging.getLogger('student_management')

class UpdateGradeView(APIView):
    def post(self, request, student_id, course_id):
        try:
            grade = request.data.get('grade')
            student = Student.objects.get(id=student_id)
            course = Course.objects.get(id=course_id)
            grade_instance = Grade.objects.create(student=student, course=course, grade=grade)
            logger.info(f"Grade updated for student {student.name} in course {course.name}")
            return Response({"message": "Grade updated"}, status=status.HTTP_200_OK)
        except Student.DoesNotExist or Course.DoesNotExist:
            return Response({"error": "Student or course not found"}, status=status.HTTP_404_NOT_FOUND)
