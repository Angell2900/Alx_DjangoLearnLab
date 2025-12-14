from django.urls import path
from .views import FollowUserAPIView, UnfollowUserAPIView

urlpatterns = [
    path('follow/<int:user_id>/', FollowUserAPIView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserAPIView.as_view(), name='unfollow-user'),
]
