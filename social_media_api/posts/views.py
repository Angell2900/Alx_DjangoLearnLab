from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from accounts.models import CustomUser
from notifications.models import Notification
from .serializers import PostSerializer, CommentSerializer

class FeedViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        # Get posts from users current user follows
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        Like.objects.get_or_create(user=request.user, post=post)
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb='liked',
            target=post
        )
        return Response({'status': 'post liked'})

    @action(detail=True, methods=['POST'])
    def unlike(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        Like.objects.filter(user=request.user, post=post).delete()
        return Response({'status': 'post unliked'})
