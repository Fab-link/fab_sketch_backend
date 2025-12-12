from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Design(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='designs')
    
    # Design metadata
    title = models.CharField(max_length=200)
    description = models.TextField()
    hashtags = models.TextField(blank=True, help_text="Space or comma separated hashtags")
    materials = models.TextField(blank=True)
    
    # Image URLs
    image_urls = models.JSONField(default=list, help_text="Array of image URLs")
    sketch_url = models.URLField(blank=True, null=True)
    tech_flat_url = models.URLField(blank=True, null=True, help_text="Technical flat design")
    try_on_url = models.URLField(blank=True, null=True, help_text="Try-on/wearing image")
    
    # Generation tracking
    session_id = models.CharField(max_length=100, blank=True, null=True, help_text="Lambda generation session ID")
    
    # Funding fields (for future use)
    funding_progress = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, help_text="Funding progress (0.0-1.0)")
    funding_amount = models.CharField(max_length=50, blank=True, default='₩0', help_text="Current funding amount")
    funding_goal = models.CharField(max_length=50, blank=True, default='₩0', help_text="Funding goal amount")
    
    # Stats
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.user.nickname}"
    
    @property
    def like_count(self):
        return self.likes.count()
    
    @property
    def comment_count(self):
        return self.comments.count()
    
    def is_liked_by(self, user):
        if user.is_anonymous:
            return False
        return self.likes.filter(user=user).exists()
    
    def is_bookmarked_by(self, user):
        if user.is_anonymous:
            return False
        return self.bookmarks.filter(user=user).exists()
