from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Like, Bookmark, Follow
from designs.models import Design

User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, design_id):
    """Toggle like for a design"""
    design = get_object_or_404(Design, id=design_id)
    like, created = Like.objects.get_or_create(
        design=design, 
        user=request.user
    )
    
    if not created:
        like.delete()
        return Response({'liked': False, 'message': 'Like removed'})
    
    return Response({'liked': True, 'message': 'Like added'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_bookmark(request, design_id):
    """Toggle bookmark for a design"""
    design = get_object_or_404(Design, id=design_id)
    bookmark, created = Bookmark.objects.get_or_create(
        design=design, 
        user=request.user
    )
    
    if not created:
        bookmark.delete()
        return Response({'bookmarked': False, 'message': 'Bookmark removed'})
    
    return Response({'bookmarked': True, 'message': 'Bookmark added'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_follow(request, user_id):
    """Toggle follow for a user"""
    if str(request.user.id) == str(user_id):
        return Response({'error': 'Cannot follow yourself'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    followee = get_object_or_404(User, id=user_id)
    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        followee=followee
    )
    
    if not created:
        follow.delete()
        return Response({'following': False, 'message': 'Unfollowed'})
    
    return Response({'following': True, 'message': 'Following'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_bookmarks(request):
    """Get user's bookmarked designs"""
    from designs.serializers import DesignSerializer
    
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('design__user')
    designs = [bookmark.design for bookmark in bookmarks]
    
    serializer = DesignSerializer(designs, many=True, context={'request': request})
    return Response(serializer.data)
