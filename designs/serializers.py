from rest_framework import serializers
from .models import Design
from users.serializers import UserSerializer

class DesignSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    
    class Meta:
        model = Design
        fields = [
            'id', 'user', 'sketch_url', 'flat_url', 'wearing_url',
            'title', 'description', 'hashtags', 'materials', 
            'view_count', 'created_at', 'like_count', 'comment_count',
            'is_liked', 'is_bookmarked'
        ]
        read_only_fields = ['id', 'user', 'view_count', 'created_at']
    
    def get_like_count(self, obj):
        return obj.likes.count()
    
    def get_comment_count(self, obj):
        return obj.comments.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
    
    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.bookmarks.filter(user=request.user).exists()
        return False

class DesignCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Design
        fields = [
            'sketch_url', 'flat_url', 'wearing_url',
            'title', 'description', 'hashtags', 'materials'
        ]
