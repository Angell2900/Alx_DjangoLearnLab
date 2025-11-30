from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    AuthorListView,
    AuthorDetailView,
)

app_name = 'api'

urlpatterns = [
    # Book endpoints
    # GET: List all books with filtering, searching, ordering
    # POST: Create a new book (authenticated users only)
    path('books/', BookListView.as_view(), name='book-list'),
    
    # GET: Retrieve a specific book by ID
    # PUT: Update entire book object (authenticated users only)
    # PATCH: Partial update of book object (authenticated users only)
    # DELETE: Delete a book (authenticated users only)
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # Author endpoints
    # GET: List all authors with their nested books
    # POST: Create a new author (authenticated users only)
    path('authors/', AuthorListView.as_view(), name='author-list'),
    
    # GET: Retrieve a specific author with their books by ID
    # PUT: Update entire author object (authenticated users only)
    # PATCH: Partial update of author object (authenticated users only)
    # DELETE: Delete an author and cascade delete their books (authenticated users only)
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
]
