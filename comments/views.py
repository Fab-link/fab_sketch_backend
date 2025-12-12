from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import Comment
from .serializers import CommentSerializer, CommentCreateSerializer
from designs.models import Design

class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        # Handle both URL parameter and query parameter
        design_id = getattr(self, 'design_id', None) or self.request.query_params.get('design_id')
        if design_id:
            return Comment.objects.filter(design_id=design_id).order_by('-created_at')
        return Comment.objects.all().order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer
    
    def list(self, request, design_id=None):
        """Get comments for a specific design"""
        if design_id:
            self.design_id = design_id
            design = get_object_or_404(Design, id=design_id)
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, design_id=None):
        """Create comment for a specific design"""
        if design_id:
            design = get_object_or_404(Design, id=design_id)
            # Add design to request data
            request.data['design'] = design.id
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user != request.user:
            return Response({'error': 'Permission denied'}, 
                          status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user != request.user:
            return Response({'error': 'Permission denied'}, 
                          status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
