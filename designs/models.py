from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Design(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='designs')
    sketch_url = models.URLField()
    flat_url = models.URLField()
    wearing_url = models.URLField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    hashtags = models.JSONField(default=list, blank=True)
    materials = models.TextField(blank=True)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} by {self.user.nickname}"
