from django.urls import path
from .views import GradeListCreateView

urlpatterns = [
    path('', GradeListCreateView.as_view(), name='grade-list-create'),
]
