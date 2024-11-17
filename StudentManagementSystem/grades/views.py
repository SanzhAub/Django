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


class GradeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        grades = Grade.objects.filter(student=request.user)
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GradeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        
class GradeCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.role != "teacher":
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        student_id = request.data.get("student")
        course_id = request.data.get("course")
        grade_value = request.data.get("grade")

        grade = Grade.objects.create(student_id=student_id, course_id=course_id, grade=grade_value)
        return Response({"detail": "Grade added successfully"}, status=status.HTTP_201_CREATED)
