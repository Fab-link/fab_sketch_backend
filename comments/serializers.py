from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'design_id', 'user_id', 'content',
            'user_nickname', 'user_profile_image',
            'created_at', 'updated_at', 'is_owner'
        ]
        read_only_fields = ['id', 'user_nickname', 'user_profile_image', 'created_at', 'updated_at']
    
    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.user == request.user
        return False

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['design', 'content']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
