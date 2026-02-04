from django.contrib import admin
from .models import SearchHistory, ToDoItem


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'search_type', 'found', 'created_at']
    list_filter = ['search_type', 'found', 'created_at']
    search_fields = ['title']
    date_hierarchy = 'created_at'


@admin.register(ToDoItem)
class ToDoItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'priority', 'completed', 'created_at']
    list_filter = ['media_type', 'priority', 'completed', 'created_at']
    search_fields = ['title', 'notes']
    date_hierarchy = 'created_at'
    actions = ['mark_completed', 'mark_incomplete']
    
    def mark_completed(self, request, queryset):
        from django.utils import timezone
        queryset.update(completed=True, completed_at=timezone.now())
    mark_completed.short_description = "Mark selected items as completed"
    
    def mark_incomplete(self, request, queryset):
        queryset.update(completed=False, completed_at=None)
    mark_incomplete.short_description = "Mark selected items as incomplete"
