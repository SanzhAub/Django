from django.urls import path, include
from .views import UserProfileView
from djoser.views import TokenCreateView
from .views import RestrictedDataView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path("api/auth/login/", TokenCreateView.as_view(), name="login"),
    path("restricted-data/", RestrictedDataView.as_view(), name="restricted-data"),
]
