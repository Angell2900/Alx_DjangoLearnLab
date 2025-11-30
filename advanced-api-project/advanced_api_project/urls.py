"""
URL Configuration for advanced_api_project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from . import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app import views
    2. Add a URL to urlpatterns:  path('', views.Home, name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def api_root(request):
    """API Root endpoint."""
    return Response({
        'message': 'Advanced Book API',
        'endpoints': {
            'books': request.build_absolute_uri('/api/books/'),
            'books_create': request.build_absolute_uri('/api/books/create/'),
            'books_update': request.build_absolute_uri('/api/books/<id>/update/'),
            'books_delete': request.build_absolute_uri('/api/books/<id>/delete/'),
            'authors': request.build_absolute_uri('/api/authors/'),
        }
    })


urlpatterns = [
    # Root API endpoint
    path('', api_root, name='api-root'),
    
    # Django admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('api.urls')),
]
