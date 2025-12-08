from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework.routers import DefaultRouter
from designs.views import DesignViewSet
from comments.views import CommentViewSet
from users.views import UserViewSet
from users import auth_views
from social import views as social_views

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
    
    # Social endpoints
    path('api/like/<int:design_id>/', social_views.toggle_like, name='toggle_like'),
    path('api/bookmark/<int:design_id>/', social_views.toggle_bookmark, name='toggle_bookmark'),
    path('api/follow/<int:user_id>/', social_views.toggle_follow, name='toggle_follow'),
    path('api/bookmarks/', social_views.user_bookmarks, name='user_bookmarks'),
    
    # Convenience endpoints matching PRD
    path('api/feed/', DesignViewSet.as_view({'get': 'feed'}), name='feed'),
    path('api/design/<int:pk>/', DesignViewSet.as_view({'get': 'retrieve'}), name='design_detail'),
    path('api/design/', DesignViewSet.as_view({'post': 'create'}), name='design_create'),
    path('api/user/<int:pk>/', UserViewSet.as_view({'get': 'profile', 'put': 'update'}), name='user_profile'),
]
