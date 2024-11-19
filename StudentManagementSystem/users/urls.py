from django.urls import path, include
from .views import UserProfileView, RestrictedDataView
from djoser.views import TokenCreateView


urlpatterns = [
    path('auth/', include('djoser.urls')),
    #path('auth/', include('djoser.urls.authtoken')),
    path('auth/token/', include('djoser.urls.authtoken')),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('restricted-data/', RestrictedDataView.as_view(), name='restricted-data'),
]

