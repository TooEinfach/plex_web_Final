"""
URL configuration for plex_checker app
"""
from django.urls import path
from . import views

app_name = 'plex_checker'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('refresh-cache/', views.refresh_cache, name='refresh_cache'),
    path('stats/', views.stats, name='stats'),
    path('todo/', views.todo_list, name='todo_list'),
    path('todo/add/', views.add_todo, name='add_todo'),
    path('todo/<int:todo_id>/toggle/', views.toggle_todo, name='toggle_todo'),
    path('todo/<int:todo_id>/delete/', views.delete_todo, name='delete_todo'),
]
