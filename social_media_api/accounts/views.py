from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.views import APIView

# User Registration
class RegisterAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

# User Login
class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

# User Profile
class ProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RegisterSerializer

    def get_object(self):
        return self.request.user

# Follow / Unfollow Users
class FollowUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = CustomUser.objects.get(id=user_id)
        request.user.following.add(user_to_follow)
        return Response({'detail': f'You are now following {user_to_follow.username}'})

class UnfollowUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_unfollow = CustomUser.objects.get(id=user_id)
        request.user.following.remove(user_to_unfollow)
        return Response({'detail': f'You have unfollowed {user_to_unfollow.username}'})
