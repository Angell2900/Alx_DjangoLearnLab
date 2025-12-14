from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from accounts.models import CustomUser
from notifications.models import Notification

# Post CRUD
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionError("You cannot edit someone else's post")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionError("You cannot delete someone else's post")
        instance.delete()

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

# Comment CRUD
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionError("You cannot edit someone else's comment")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionError("You cannot delete someone else's comment")
        instance.delete()

# Feed view for posts from users you follow
class FeedViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
