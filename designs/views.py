from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import F
from .models import Design
from .serializers import DesignSerializer, DesignCreateSerializer

class DesignViewSet(viewsets.ModelViewSet):
    queryset = Design.objects.select_related('user').prefetch_related('likes', 'bookmarks', 'comments')
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DesignCreateSerializer
        return DesignSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        # Increment view count
        instance = self.get_object()
        Design.objects.filter(pk=instance.pk).update(view_count=F('view_count') + 1)
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def feed(self, request):
        """Random feed for home page"""
        designs = self.get_queryset().order_by('?')  # Random order
        page = self.paginate_queryset(designs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(designs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def user_designs(self, request):
        """Get designs by user ID"""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id parameter required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        designs = self.get_queryset().filter(user_id=user_id)
        page = self.paginate_queryset(designs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(designs, many=True)
        return Response(serializer.data)
