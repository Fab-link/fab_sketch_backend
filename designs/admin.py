from django.contrib import admin
from .models import Design

@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'view_count', 'like_count', 'comment_count', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['title', 'description', 'user__nickname']
    readonly_fields = ['view_count', 'created_at', 'like_count', 'comment_count']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'title', 'description')
        }),
        ('Images', {
            'fields': ('sketch_url', 'flat_url', 'wearing_url')
        }),
        ('Details', {
            'fields': ('hashtags', 'materials')
        }),
        ('Stats', {
            'fields': ('view_count', 'like_count', 'comment_count', 'created_at'),
            'classes': ('collapse',)
        })
    )
    
    def like_count(self, obj):
        return obj.likes.count()
    like_count.short_description = 'Likes'
    
    def comment_count(self, obj):
        return obj.comments.count()
    comment_count.short_description = 'Comments'
