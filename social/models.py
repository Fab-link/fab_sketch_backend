from django.db import models
from django.contrib.auth import get_user_model
from designs.models import Design

User = get_user_model()

class Like(models.Model):
    design = models.ForeignKey(Design, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('design', 'user')
    
    def __str__(self):
        return f"{self.user.nickname} likes {self.design.title}"

class Bookmark(models.Model):
    design = models.ForeignKey(Design, on_delete=models.CASCADE, related_name='bookmarks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('design', 'user')
    
    def __str__(self):
        return f"{self.user.nickname} bookmarked {self.design.title}"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'followee')
        constraints = [
            models.CheckConstraint(
                check=~models.Q(follower=models.F('followee')),
                name='prevent_self_follow'
            )
        ]
    
    def __str__(self):
        return f"{self.follower.nickname} follows {self.followee.nickname}"
