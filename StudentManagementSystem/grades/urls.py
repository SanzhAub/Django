from django.urls import path
from .views import GradeListCreateView
from .views import GradeCreateView

urlpatterns = [
    path('', GradeListCreateView.as_view(), name='grade-list-create'),
    path("", GradeCreateView.as_view(), name="add-grade"),
]
