from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, LibraryDetailView, admin_view, librarian_view, member_view
from . import views
from django.contrib import admin


urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    
    path('admin/', admin_view, name='admin_view'),
    path('librarian/', librarian_view, name='librarian_view'),
    path('member/', member_view, name='member_view'),
]   
path('', include('relationship_app.urls')),
path('books/add/', views.add_book, name='add_book'),
path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),

