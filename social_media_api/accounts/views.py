from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class FollowUserAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = CustomUser.objects.get(id=user_id)
        request.user.following.add(target_user)
        return Response({'status': f'You are now following {target_user.username}'})

class UnfollowUserAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = CustomUser.objects.get(id=user_id)
        request.user.following.remove(target_user)
        return Response({'status': f'You have unfollowed {target_user.username}'})
