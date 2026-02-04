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
]
