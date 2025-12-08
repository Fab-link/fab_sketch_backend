from django.db import models
from django.contrib.auth import get_user_model
from designs.models import Design

User = get_user_model()

class Comment(models.Model):
    design = models.ForeignKey(Design, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.user.nickname} on {self.design.title}"
