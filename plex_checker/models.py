from django.db import models


class SearchHistory(models.Model):
    """Track search history for analytics"""
    title = models.CharField(max_length=500)
    found = models.BooleanField(default=False)
    search_type = models.CharField(max_length=20, choices=[
        ('exact', 'Exact'),
        ('fuzzy', 'Fuzzy'),
        ('server', 'Server')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Search histories'
    
    def __str__(self):
        return f"{self.title} - {self.search_type} - {'Found' if self.found else 'Not Found'}"


class ToDoItem(models.Model):
    """Track media to add to Plex server"""
    title = models.CharField(max_length=500)
    media_type = models.CharField(max_length=20, choices=[
        ('movie', 'Movie'),
        ('tv', 'TV Show'),
        ('music', 'Music'),
        ('other', 'Other')
    ], default='movie')
    notes = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], default='medium')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        status = "✓" if self.completed else "☐"
        return f"{status} {self.title} ({self.media_type})"
