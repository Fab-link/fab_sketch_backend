from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    follower_count = serializers.CharField(source='formatted_follower_count', read_only=True)
    following_count = serializers.CharField(source='formatted_following_count', read_only=True)
    post_count = serializers.CharField(source='formatted_design_count', read_only=True)
    is_following = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'user_id', 'nickname', 'profile_image', 'bio', 'location',
            'created_at', 'follower_count', 'following_count', 'post_count', 'is_following'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.followers.filter(follower=request.user).exists()
        return False

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['user_id', 'nickname', 'password', 'profile_image', 'bio', 'location']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
