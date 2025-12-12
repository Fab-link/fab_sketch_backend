from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Like, Bookmark, Follow
from .serializers import LikeSerializer, BookmarkSerializer, FollowSerializer
from designs.models import Design

User = get_user_model()

class LikeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer
    
    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)
    
    def toggle(self, request, design_id=None):
        """Toggle like for a design (URL parameter)"""
        design = get_object_or_404(Design, id=design_id)
        like, created = Like.objects.get_or_create(
            design=design, 
            user=request.user
        )
        
        if not created:
            like.delete()
            return Response({'liked': False, 'message': 'Like removed'})
        
        return Response({'liked': True, 'message': 'Like added'})

class BookmarkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BookmarkSerializer
    
    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user).select_related('design')
    
    def toggle(self, request, design_id=None):
        """Toggle bookmark for a design (URL parameter)"""
        design = get_object_or_404(Design, id=design_id)
        bookmark, created = Bookmark.objects.get_or_create(
            design=design, 
            user=request.user
        )
        
        if not created:
            bookmark.delete()
            return Response({'bookmarked': False, 'message': 'Bookmark removed'})
        
        return Response({'bookmarked': True, 'message': 'Bookmark added'})
    
    def user_bookmarks(self, request, user_id=None):
        """Get user's bookmarked designs"""
        user = get_object_or_404(User, id=user_id) if user_id else request.user
        bookmarks = Bookmark.objects.filter(user=user).select_related('design', 'design__user')
        
        # Return design data with bookmark info
        designs = []
        for bookmark in bookmarks:
            design_data = {
                'id': bookmark.design.id,
                'title': bookmark.design.title,
                'description': bookmark.design.description,
                'image_urls': bookmark.design.image_urls,
                'user_id': bookmark.design.user.user_id,
                'created_at': bookmark.design.created_at,
                'bookmarked_at': bookmark.created_at,
            }
            designs.append(design_data)
        
        return Response(designs)

class FollowViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer
    
    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user).select_related('followee')
    
    def toggle(self, request, user_id=None):
        """Toggle follow for a user (URL parameter)"""
        followee = get_object_or_404(User, id=user_id)
        if followee == request.user:
            return Response({'error': 'Cannot follow yourself'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        follow, created = Follow.objects.get_or_create(
            follower=request.user, 
            followee=followee
        )
        
        if not created:
            follow.delete()
            return Response({'following': False, 'message': 'Unfollowed'})
        
        return Response({'following': True, 'message': 'Following'})
