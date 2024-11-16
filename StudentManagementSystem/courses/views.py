from rest_framework import generics
from courses.models import Course, Enrollment
from courses.serializers import CourseSerializer, EnrollmentSerializer
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

@method_decorator(cache_page(60 * 15), name='dispatch')  # Cache for 15 minutes
class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

class EnrollmentCreateView(generics.CreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

logger = logging.getLogger('student_management')

class EnrollInCourseView(APIView):
    def post(self, request, course_id):
        student = request.user.student
        try:
            course = Course.objects.get(id=course_id)
            student.courses.add(course)
            logger.info(f"Student {student.name} enrolled in course {course.name}")  # Log enrollment
            return Response({"message": "Enrolled successfully"}, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)


