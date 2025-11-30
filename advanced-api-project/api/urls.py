from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    AuthorListView,
    AuthorDetailView,
)

app_name = 'api'

urlpatterns = [
    # ========================================================================
    # BOOK ENDPOINTS
    # ========================================================================
    
    # List all books and create new books
    # GET:  /api/books/              - List all books with filtering/search/order
    # POST: /api/books/              - Create new book (authenticated only)
    path('books/', BookListView.as_view(), name='book-list'),
    
    # Retrieve, update, or delete a specific book
    # GET:    /api/books/<id>/       - Retrieve book by ID
    # PUT:    /api/books/<id>/       - Update entire book (authenticated only)
    # PATCH:  /api/books/<id>/       - Partial update book (authenticated only)
    # DELETE: /api/books/<id>/       - Delete book (authenticated only)
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # ========================================================================
    # AUTHOR ENDPOINTS
    # ========================================================================
    
    # List all authors and create new authors
    # GET:  /api/authors/            - List all authors with nested books
    # POST: /api/authors/            - Create new author (authenticated only)
    path('authors/', AuthorListView.as_view(), name='author-list'),
    
    # Retrieve, update, or delete a specific author
    # GET:    /api/authors/<id>/     - Retrieve author with books
    # PUT:    /api/authors/<id>/     - Update entire author (authenticated only)
    # PATCH:  /api/authors/<id>/     - Partial update author (authenticated only)
    # DELETE: /api/authors/<id>/     - Delete author and cascade delete books
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
]
