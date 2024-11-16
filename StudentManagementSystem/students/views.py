from rest_framework.views import APIView
from rest_framework.response import Response
from users.permissions import IsStudent
from rest_framework import generics
from students.models import Student
from students.serializers import StudentSerializer
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache

class StudentProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        cache_key = f"student_profile_{pk}"
        student_data = cache.get(cache_key)

        if not student_data:
            try:
                student = Student.objects.get(pk=pk)
                serializer = StudentSerializer(student)
                student_data = serializer.data
                cache.set(cache_key, student_data, timeout=60 * 10)  # Cache for 10 minutes
            except Student.DoesNotExist:
                return Response({"error": "Student not found"}, status=404)

        return Response(student_data)
class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

class StudentDetailView(generics.RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save()
        cache_key = f"student_profile_{instance.pk}"
        cache.delete(cache_key)  # Invalidate cache