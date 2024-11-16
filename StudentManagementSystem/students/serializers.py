from rest_framework import serializers
from students.models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user', 'date_of_birth', 'registration_date']
        read_only_fields = ['registration_date']
