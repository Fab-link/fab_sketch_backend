from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentCreateSerializer
from designs.models import Design

class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer
    
    def get_queryset(self):
        design_id = self.request.query_params.get('design_id')
        if design_id:
            return Comment.objects.filter(design_id=design_id).select_related('user')
        return Comment.objects.select_related('user')
    
    def perform_create(self, serializer):
        design_id = self.request.data.get('design_id')
        try:
            design = Design.objects.get(id=design_id)
            serializer.save(user=self.request.user, design=design)
        except Design.DoesNotExist:
            return Response({'error': 'Design not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
    
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
