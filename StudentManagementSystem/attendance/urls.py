from django.urls import path
from .views import AttendanceListCreateView
from .views import MarkAttendanceView

urlpatterns = [
    path('', AttendanceListCreateView.as_view(), name='attendance-list-create'),
    path("mark/<int:course_id>/", MarkAttendanceView.as_view(), name="mark-attendance"),
]
