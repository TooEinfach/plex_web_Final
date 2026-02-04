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
