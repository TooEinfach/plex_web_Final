from django.contrib import admin
from .models import SearchHistory


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'search_type', 'found', 'created_at']
    list_filter = ['search_type', 'found', 'created_at']
    search_fields = ['title']
    date_hierarchy = 'created_at'
