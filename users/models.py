from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    user_id = models.CharField(max_length=150, unique=True, help_text="Unique user ID for login")
    nickname = models.CharField(max_length=50, help_text="Display name")
    profile_image = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, default='Seoul, Korea')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nickname} ({self.user_id})"
    
    @property
    def design_count(self):
        return self.designs.count()
    
    @property
    def follower_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.following.count()
    
    def format_count(self, count):
        """Format count as 1.2K, 500M etc."""
        if count >= 1000000:
            return f'{count / 1000000:.1f}M'
        elif count >= 1000:
            return f'{count / 1000:.1f}K'
        return str(count)
    
    @property
    def formatted_design_count(self):
        return self.format_count(self.design_count)
    
    @property
    def formatted_follower_count(self):
        return self.format_count(self.follower_count)
    
    @property
    def formatted_following_count(self):
        return self.format_count(self.following_count)
