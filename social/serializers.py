from rest_framework import serializers
from .models import Like, Bookmark, Follow

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'design_id', 'user_id', 'created_at']
        read_only_fields = ['id', 'created_at']

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['id', 'design_id', 'user_id', 'created_at']
        read_only_fields = ['id', 'created_at']

class FollowSerializer(serializers.ModelSerializer):
    follower_nickname = serializers.CharField(source='follower.nickname', read_only=True)
    followee_nickname = serializers.CharField(source='followee.nickname', read_only=True)
    
    class Meta:
        model = Follow
        fields = [
            'id', 'follower_id', 'followee_id', 
            'follower_nickname', 'followee_nickname', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
