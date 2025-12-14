from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Simple home view for root URL
def home(request):
    return HttpResponse("Welcome to the Social Media API!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),  # Accounts app: register, login, profile, follow/unfollow
    path('api/posts/', include('posts.urls')),        # Posts app: CRUD, feed, like/unlike
    path('', home),                                   # Root URL
]
