from django.db.models.signals import post_save
from django.dispatch import receiver
from grades.models import Grade
from notifications.tasks import send_grade_update_notification

@receiver(post_save, sender=Grade)
def notify_student_grade_updated(sender, instance, created, **kwargs):
    """Send a notification when a grade is updated."""
    if not created:  # Notify only on updates
        student_email = instance.student.email
        course_name = instance.course.name
        grade = instance.grade
        
        # Trigger the Celery task
        send_grade_update_notification.delay(student_email, course_name, grade)
