"""Определяет схемы URL для learning_logs."""
from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    # Домашняя страница
    path('', views.index, name='index'),
    # Список всех тем
    path('topics/', views.topics, name='topics'),
    # Одна тема
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # Новая тема
    path('new_topic/', views.new_topic, name='new_topic'),
    # Удаление темы
    path('delete_topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),
    # Новая запись
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # Редактирование записи
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    # Удаление записи
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
]
