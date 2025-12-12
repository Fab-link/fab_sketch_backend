from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Comment(models.Model):
    design = models.ForeignKey('designs.Design', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    
    # Denormalized user info for performance
    user_nickname = models.CharField(max_length=50)
    user_profile_image = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['design_id']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"Comment by {self.user_nickname} on {self.design.title}"
    
    def save(self, *args, **kwargs):
        # Auto-populate denormalized fields
        if not self.user_nickname:
            self.user_nickname = self.user.nickname
        if not self.user_profile_image:
            self.user_profile_image = self.user.profile_image
        super().save(*args, **kwargs)
