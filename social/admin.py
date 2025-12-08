from django.contrib import admin
from .models import Like, Bookmark, Follow

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'design', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__nickname', 'design__title']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'design', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__nickname', 'design__title']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'followee', 'created_at']
    list_filter = ['created_at']
    search_fields = ['follower__nickname', 'followee__nickname']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('follower', 'followee')
