from django.urls import path
from .views import CourseListCreateView, EnrollmentCreateView

urlpatterns = [
    path('', CourseListCreateView.as_view(), name='course-list-create'),
    path('enroll/', EnrollmentCreateView.as_view(), name='enroll-student'),
]
