from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),  # Список всех постов
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # Просмотр одного поста
    path('post/new/', views.post_create, name='post_create'),  # Создание нового поста
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),  # Редактирование поста
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),  # Удаление поста
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),  # Добавление комментария
]
