from django.contrib import admin
from django.urls import path, include
from api.views import api_root

urlpatterns = [
    # Root API endpoint
    path('', api_root, name='api-root'),
    
    # Django admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('api.urls')),
]
