from django.db import models
from users.models import User  # Assuming a custom User model
from courses.models import Course  # Assuming Course model exists

class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    grade = models.CharField(max_length=2)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='given_grades')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.name} - {self.grade}"


