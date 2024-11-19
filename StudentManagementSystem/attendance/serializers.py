from rest_framework import serializers
from attendance.models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'course', 'date', 'status']

    def validate_present(self, value):
        if value not in [True, False]:
            raise serializers.ValidationError("Invalid value for 'present' (must be True or False).")
        return value