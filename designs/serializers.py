from rest_framework import serializers
from .models import Design
from users.serializers import UserSerializer

class DesignSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    
    # Flutter app compatibility fields
    id = serializers.CharField(source='pk', read_only=True)
    user_id = serializers.CharField(source='user.user_id', read_only=True)
    likes = serializers.IntegerField(source='like_count', read_only=True)
    comments = serializers.IntegerField(source='comment_count', read_only=True)
    tags = serializers.CharField(source='hashtags', read_only=True)
    
    # Flattened designer fields for easy access
    designer_nickname = serializers.CharField(source='user.nickname', read_only=True)
    designer_profile_image = serializers.CharField(source='user.profile_image', read_only=True)
    designer_follower_count = serializers.SerializerMethodField()
    designer_following_count = serializers.SerializerMethodField()
    designer_post_count = serializers.SerializerMethodField()
    is_following_designer = serializers.SerializerMethodField()
    
    class Meta:
        model = Design
        fields = [
            'id', 'user', 'user_id', 'title', 'description', 'hashtags', 'materials',
            'image_urls', 'sketch_url', 'tech_flat_url', 'try_on_url',
            'session_id', 'funding_progress', 'funding_amount', 'funding_goal',
            'view_count', 'created_at', 'updated_at',
            'like_count', 'comment_count', 'is_liked', 'is_bookmarked',
            'likes', 'comments', 'tags',
            'designer_nickname', 'designer_profile_image', 'designer_follower_count',
            'designer_following_count', 'designer_post_count', 'is_following_designer'
        ]
        read_only_fields = ['id', 'user', 'view_count', 'created_at']
    
    def get_like_count(self, obj):
        return obj.like_count
    
    def get_comment_count(self, obj):
        return obj.comment_count
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.is_liked_by(request.user)
        return False
    
    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.is_bookmarked_by(request.user)
        return False
    
    def get_designer_follower_count(self, obj):
        return obj.user.followers.count()
    
    def get_designer_following_count(self, obj):
        return obj.user.following.count()
    
    def get_designer_post_count(self, obj):
        return obj.user.designs.count()
    
    def get_is_following_designer(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user != obj.user:
            return obj.user.followers.filter(follower=request.user).exists()
        return False

class DesignCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Design
        fields = [
            'sketch_url', 'image_url', 'tech_flat_url', 'try_on_url',
            'title', 'description', 'hashtags', 'materials', 'session_id'
        ]
