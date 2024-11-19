from djoser.serializers import UserCreateSerializer, UserSerializer
from .models import User
from rest_framework import serializers

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'password', 'email', 'role')

    def validate_role(self, value):
        if value not in ['student', 'teacher', 'admin']:
            raise serializers.ValidationError("Invalid role")
        return value

class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'role')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']
