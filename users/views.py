from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserCreateSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user != request.user:
            return Response({'error': 'Permission denied'}, 
                          status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        """Get user profile with stats"""
        user = self.get_object()
        serializer = self.get_serializer(user)
        data = serializer.data
        
        # Add social stats
        data['followers_count'] = user.followers.count()
        data['following_count'] = user.following.count()
        data['designs_count'] = user.designs.count()
        
        # Check if current user follows this user
        if request.user.is_authenticated:
            data['is_following'] = user.followers.filter(follower=request.user).exists()
        else:
            data['is_following'] = False
            
        return Response(data)
