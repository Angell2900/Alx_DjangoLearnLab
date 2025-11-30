from django.shortcuts import render
from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class BookListView(generics.ListCreateAPIView):
    """
    API view for listing and creating Book instances.
    
    This generic view handles two main HTTP methods:
    1. GET: Retrieve a paginated list of all books with filtering, searching, and ordering
    2. POST: Create a new book (requires authentication)
    
    Advanced Query Capabilities:
        
        FILTERING:
        - Filter by author ID: ?author=1
        - Filter by publication_year: ?publication_year=1997
        - Combine filters: ?author=1&publication_year=1997
        
        SEARCHING:
        - Search by book title: ?search=Harry
        - Search by author name: ?search=Rowling
        
        ORDERING:
        - Order by title (ascending): ?ordering=title
        - Order by title (descending): ?ordering=-title
        - Order by publication year (ascending): ?ordering=publication_year
        - Order by publication year (descending): ?ordering=-publication_year
        - Multiple fields: ?ordering=-publication_year,title
        
        PAGINATION:
        - Default 10 items per page
        - Access page 2: ?page=2
    
    Features:
        - Pagination: 10 items per page (configurable via DEFAULT_PAGE_SIZE in settings)
        - Filtering: By author ID and publication_year
        - Search: On book title and author name
        - Ordering: By title and publication_year (default: descending publication_year)
        - Query optimization: Uses select_related('author') to avoid N+1 queries
    
    Permissions:
        - GET: Open to all users (authenticated and unauthenticated)
        - POST: Restricted to authenticated users only (IsAuthenticatedOrReadOnly)
    
    Query Parameters Examples:
        GET /api/books/ - Get all books
        GET /api/books/?author=1 - Filter by author ID
        GET /api/books/?publication_year=1997 - Filter by publication year
        GET /api/books/?search=Harry - Search for books containing "Harry" in title or author name
        GET /api/books/?ordering=publication_year - Order by publication year ascending
        GET /api/books/?ordering=-title - Order by title descending
        
        POST /api/books/ - Create a new book (requires authentication)
        Headers: Authorization: Token YOUR_TOKEN
        Body: {
            "title": "The Hobbit",
            "publication_year": 1937,
            "author": 1
        }
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # Configure filtering, searching, and ordering
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'created_at']
    ordering = ['-publication_year', 'title']

    def perform_create(self, serializer):
        """
        Save the book instance when it's created.
        
        This method is called after validation passes during a POST request.
        Override this to add custom logic before saving (e.g., logging, signals).
        
        Args:
            serializer: The validated serializer instance
        """
        serializer.save()


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a single Book instance.
    
    This generic view handles three main HTTP methods:
    1. GET: Retrieve a single book by ID
    2. PUT/PATCH: Update an existing book (requires authentication)
    3. DELETE: Delete a book (requires authentication)
    
    Features:
        - Query optimization: Uses select_related('author') to avoid N+1 queries
        - Full CRUD support: Retrieve, Update, Delete operations
        - PATCH support: Partial updates of book fields
        - Automatic 404 handling: Returns 404 if book not found
    
    Permissions:
        - GET: Open to all users
        - PUT/PATCH/DELETE: Restricted to authenticated users only
    
    URL Pattern Examples:
        GET /api/books/1/ - Retrieve book with ID 1
        PUT /api/books/1/ - Update entire book with ID 1 (requires authentication)
        PATCH /api/books/1/ - Partial update of book with ID 1 (requires authentication)
        DELETE /api/books/1/ - Delete book with ID 1 (requires authentication)
    
    Request Body Examples:
        PUT/PATCH:
        {
            "title": "Updated Title",
            "publication_year": 1998,
            "author": 1
        }
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        """
        Save the updated book instance.
        
        This method is called after validation passes during a PUT or PATCH request.
        Override this to add custom logic before saving.
        
        Args:
            serializer: The validated serializer instance
        """
        serializer.save()


class AuthorListView(generics.ListCreateAPIView):
    """
    API view for listing and creating Author instances.
    
    This generic view handles two main HTTP methods:
    1. GET: Retrieve a paginated list of all authors with their nested books
    2. POST: Create a new author (requires authentication)
    
    Features:
        - Pagination: 10 items per page
        - Nested serialization: Each author includes all related books
        - Search: On author name
        - Ordering: By name and creation date
        - Query optimization: Uses prefetch_related('books') to optimize nested queries
    
    Permissions:
        - GET: Open to all users
        - POST: Restricted to authenticated users only
    
    Query Parameters Examples:
        GET /api/authors/ - Get all authors
        GET /api/authors/?search=Tolkien - Search for authors matching "Tolkien"
        GET /api/authors/?ordering=name - Order by author name ascending
        GET /api/authors/?ordering=-created_at - Order by creation date descending
        
        POST /api/authors/ - Create a new author (requires authentication)
        Headers: Authorization: Token YOUR_TOKEN
        Body: {
            "name": "Isaac Asimov"
        }
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a single Author instance.
    
    This generic view handles three main HTTP methods:
    1. GET: Retrieve a single author and their books by ID
    2. PUT/PATCH: Update an existing author (requires authentication)
    3. DELETE: Delete an author (requires authentication)
    
    Features:
        - Query optimization: Uses prefetch_related('books') for nested data
        - Full CRUD support: Retrieve, Update, Delete operations
        - Nested serialization: Includes all author's books in the response
        - CASCADE delete: Deleting an author also deletes all their books
    
    Permissions:
        - GET: Open to all users
        - PUT/PATCH/DELETE: Restricted to authenticated users only
    
    Note:
        When an author is deleted, all their associated books will be
        deleted due to CASCADE delete behavior defined in the Book model
    
    URL Pattern Examples:
        GET /api/authors/1/ - Retrieve author with ID 1 and all their books
        PUT /api/authors/1/ - Update entire author with ID 1 (requires authentication)
        PATCH /api/authors/1/ - Partial update of author with ID 1 (requires authentication)
        DELETE /api/authors/1/ - Delete author with ID 1 and cascade delete their books
    
    Request Body Examples:
        PUT/PATCH:
        {
            "name": "Updated Author Name"
        }
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
