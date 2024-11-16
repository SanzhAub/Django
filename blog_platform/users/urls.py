from django.urls import path, reverse
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth import views as auth_views

class CustomLoginView(auth_views.LoginView):
    def get_success_url(self):
        return reverse('profile_view', kwargs={'username': self.request.user.username})


urlpatterns = [
    path('register/', views.register, name='register'),  # Регистрация пользователя
    path('profile/<str:username>/', views.profile_view, name='profile_view'),  # Просмотр профиля пользователя
    #path('profile/edit/', views.profile_edit, name='profile_edit'),  # Редактирование профиля
    path('profile/edit/<str:username>/', views.profile_edit, name='profile_edit'),
    #path('profile/', views.profile, name='profile'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),  # Подписка на пользователя
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),  # Отписка от пользователя
    #path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),  # Login view
    path('logout/', auth_views.LogoutView.as_view(next_page='post_list'), name='logout'),  # Logout view
    path('login/', CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
]

