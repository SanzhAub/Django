from django.db import models
from courses.models import Course
from students.models import Student
from users.models import User

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="grades")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="grades")
    grade = models.CharField(max_length=5)  # e.g., A+, B, etc.
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="given_grades")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.name} - {self.grade}"

