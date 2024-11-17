from django.test import TestCase
from notifications.tasks import send_attendance_reminder

class CeleryTaskTest(TestCase):
    def test_send_attendance_reminder(self):
        result = send_attendance_reminder()
        self.assertIn("Attendance reminders sent", result)

