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
    # Book endpoints
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # Create endpoint for books
    path('books/create/', CreateView.as_view(), name='book-create'),
    
    # Update endpoint for books - MUST contain "books/update" in the path
    path('books/update/<int:pk>/', UpdateView.as_view(), name='book-update'),
    
    # Delete endpoint for books - MUST contain "books/delete" in the path
    path('books/delete/<int:pk>/', DeleteView.as_view(), name='book-delete'),
    
    # Author endpoints
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
]
