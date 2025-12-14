from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', PostViewSet.as_view({'get': 'feed'}), name='feed'),
    path('posts/<int:pk>/like/', PostViewSet.as_view({'post': 'like'}), name='like-post'),
    path('posts/<int:pk>/unlike/', PostViewSet.as_view({'post': 'unlike'}), name='unlike-post'),
]
