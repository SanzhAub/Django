from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now, localdate
from attendance.models import Attendance
from users.models import User

@shared_task
def send_attendance_reminder():
    today = localdate()
    
    students = User.objects.filter(role='student', is_active=True)
    
    missing_attendance_students = [
        student for student in students 
        if not Attendance.objects.filter(student=student, date=today).exists()
    ]
    
    for student in missing_attendance_students:
        send_mail(
            subject='Attendance Reminder',
            message='Hi {}, please mark your attendance for today.'.format(student.username),
            from_email='admin@studentmanagementsystem.com',
            recipient_list=[student.email],
            fail_silently=False,
        )
    return f'Attendance reminders sent to {len(missing_attendance_students)} students'

@shared_task
def send_grade_update_notification(student_email, course_name, grade):
    send_mail(
        subject='Grade Update Notification',
        message=f'Your grade for the course "{course_name}" has been updated to {grade}.',
        from_email='admin@studentmanagementsystem.com',
        recipient_list=[student_email],
        fail_silently=False,
    )
    return f'Grade update notification sent to {student_email}'