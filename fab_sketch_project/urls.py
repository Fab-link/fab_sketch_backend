from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework.routers import DefaultRouter
from designs.views import DesignViewSet
from designs import generation_views
from comments.views import CommentViewSet
from users.views import UserViewSet
from users import auth_views
from social.views import LikeViewSet, BookmarkViewSet, FollowViewSet

def health_check(request):
    return JsonResponse({'status': 'healthy'})

router = DefaultRouter()
router.register(r'designs', DesignViewSet)
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
    path('api/', include(router.urls)),
    
    # Authentication endpoints
    path('api/auth/register/', auth_views.register, name='register'),
    path('api/auth/login/', auth_views.login_view, name='login'),
    path('api/auth/logout/', auth_views.logout_view, name='logout'),
    path('api/auth/me/', auth_views.me, name='me'),
    
    # Design generation endpoints
    path('api/generate/', generation_views.generate_design, name='generate_design'),
    path('api/save-design/', generation_views.save_design_to_feed, name='save_design_to_feed'),
    path('api/generation-status/<str:session_id>/', generation_views.get_generation_status, name='generation_status'),
    
    # PRD-compatible endpoints
    path('api/feed/', DesignViewSet.as_view({'get': 'feed'}), name='feed'),
    path('api/design/<int:pk>/', DesignViewSet.as_view({'get': 'retrieve'}), name='design_detail'),
    path('api/design/', DesignViewSet.as_view({'post': 'create'}), name='design_create'),
    path('api/user/<int:pk>/', UserViewSet.as_view({'get': 'profile', 'put': 'update'}), name='user_profile'),
    
    # Social endpoints (simple toggle)
    path('api/like/<int:design_id>/', LikeViewSet.as_view({'post': 'toggle'}), name='toggle_like'),
    path('api/bookmark/<int:design_id>/', BookmarkViewSet.as_view({'post': 'toggle'}), name='toggle_bookmark'),
    path('api/follow/<int:user_id>/', FollowViewSet.as_view({'post': 'toggle'}), name='toggle_follow'),
    
    # Comment endpoints
    path('api/comment/<int:design_id>/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='design_comments'),
    path('api/comment/<int:pk>/', CommentViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='comment_detail'),
    
    # User content endpoints
    path('api/bookmark/<int:user_id>/', BookmarkViewSet.as_view({'get': 'user_bookmarks'}), name='user_bookmarks'),
]
