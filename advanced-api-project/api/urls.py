from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    AuthorListView,
    AuthorDetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

app_name = 'api'

urlpatterns = [
    # Book endpoints with filtering, searching, and ordering
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # Create endpoint for books
    path('books/create/', CreateView.as_view(), name='book-create'),
    
    # Update endpoint for books
    path('books/update/<int:pk>/', UpdateView.as_view(), name='book-update'),
    
    # Delete endpoint for books
    path('books/delete/<int:pk>/', DeleteView.as_view(), name='book-delete'),
    
    # Author endpoints with searching and ordering
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
]
