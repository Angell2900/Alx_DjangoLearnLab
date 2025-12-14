from django.urls import path
from .views import RegisterAPIView, LoginAPIView, FollowUserAPIView, UnfollowUserAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('follow/<int:user_id>/', FollowUserAPIView.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', UnfollowUserAPIView.as_view(), name='unfollow'),
]
