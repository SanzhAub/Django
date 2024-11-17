from django.urls import path
from .views import AttendanceListCreateView, MarkAttendanceView

urlpatterns = [
    path('', AttendanceListCreateView.as_view(), name='attendance-list-create'),
    path("mark/<int:course_id>/", MarkAttendanceView.as_view(), name="mark-attendance"),
    #path('mark/<int:id>/', MarkAttendanceView.as_view(), name='mark-attendance'),
]

