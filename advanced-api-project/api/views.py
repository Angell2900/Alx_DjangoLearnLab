from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


@api_view(['GET'])
def api_root(request):
    """
    API Root endpoint providing links to all available resources.
    """
    return Response({
        'message': 'Welcome to the Advanced Book API',
        'endpoints': {
            'books': request.build_absolute_uri('/api/books/'),
            'authors': request.build_absolute_uri('/api/authors/'),
            'admin': request.build_absolute_uri('/admin/'),
        },
        'documentation': {
            'filtering': 'Add ?author=1 or ?publication_year=1997',
            'searching': 'Add ?search=keyword',
            'ordering': 'Add ?ordering=title or ?ordering=-publication_year',
        }
    })


# ============================================================================
# BOOK VIEWS - CRUD Operations with Filtering, Searching, and Ordering
# ============================================================================

class BookListView(generics.ListCreateAPIView):
    """
    BOOK LIST VIEW
    
    HTTP Methods:
        - GET: Retrieve a paginated list of all books
        - POST: Create a new book (authenticated users only)
    
    Features:
        - Pagination: 10 items per page
        - Filtering: By author ID and publication_year
        - Searching: By book title and author name
        - Ordering: By title and publication_year
        - Query optimization: Uses select_related('author')
    
    Permissions:
        - GET: Open to all users
        - POST: Authenticated users only
    
    Query Parameters:
        - author: Filter by author ID (e.g., ?author=1)
        - publication_year: Filter by year (e.g., ?publication_year=1997)
        - search: Search by title or author (e.g., ?search=Harry)
        - ordering: Order results (e.g., ?ordering=-publication_year)
        - page: Pagination (e.g., ?page=2)
    
    Example Requests:
        GET /api/books/
        GET /api/books/?author=1&publication_year=1997
        GET /api/books/?search=Harry
        POST /api/books/ (with authentication)
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # Configure filtering, searching, and ordering backends
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    
    # Specify which fields can be filtered
    filterset_fields = ['author', 'publication_year']
    
    # Specify which fields can be searched
    search_fields = ['title', 'author__name']
    
    # Specify which fields can be ordered
    ordering_fields = ['title', 'publication_year', 'created_at']
    
    # Default ordering when no ordering parameter provided
    ordering = ['-publication_year', 'title']

    def perform_create(self, serializer):
        """
        Hook called after serializer validation during POST.
        
        Can be overridden to add custom logic before saving.
        Currently just saves the serializer data.
        """
        serializer.save()


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    BOOK DETAIL VIEW
    
    HTTP Methods:
        - GET: Retrieve a single book by ID
        - PUT: Update entire book (authenticated users only)
        - PATCH: Partial update of book (authenticated users only)
        - DELETE: Delete book (authenticated users only)
    
    Features:
        - Query optimization: Uses select_related('author')
        - Full CRUD support on individual books
        - Automatic 404 handling for non-existent books
    
    Permissions:
        - GET: Open to all users
        - PUT/PATCH/DELETE: Authenticated users only
    
    Example Requests:
        GET /api/books/1/
        PUT /api/books/1/ (with authentication)
        PATCH /api/books/1/ (with authentication)
        DELETE /api/books/1/ (with authentication)
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        """
        Hook called after serializer validation during PUT/PATCH.
        
        Can be overridden to add custom logic before saving.
        Currently just saves the serializer data.
        """
        serializer.save()


# ============================================================================
# AUTHOR VIEWS - CRUD Operations with Nested Books
# ============================================================================

class AuthorListView(generics.ListCreateAPIView):
    """
    AUTHOR LIST VIEW
    
    HTTP Methods:
        - GET: Retrieve a paginated list of all authors with nested books
        - POST: Create a new author (authenticated users only)
    
    Features:
        - Pagination: 10 items per page
        - Nested serialization: Each author includes all related books
        - Searching: By author name
        - Ordering: By name and creation date
        - Query optimization: Uses prefetch_related('books')
    
    Permissions:
        - GET: Open to all users
        - POST: Authenticated users only
    
    Query Parameters:
        - search: Search by author name (e.g., ?search=Rowling)
        - ordering: Order results (e.g., ?ordering=name)
        - page: Pagination (e.g., ?page=2)
    
    Example Requests:
        GET /api/authors/
        GET /api/authors/?search=Tolkien
        POST /api/authors/ (with authentication)
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # Configure searching and ordering backends
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
    # Specify which fields can be searched
    search_fields = ['name']
    
    # Specify which fields can be ordered
    ordering_fields = ['name', 'created_at']
    
    # Default ordering by name
    ordering = ['name']


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    AUTHOR DETAIL VIEW
    
    HTTP Methods:
        - GET: Retrieve a single author and their books by ID
        - PUT: Update entire author (authenticated users only)
        - PATCH: Partial update of author (authenticated users only)
        - DELETE: Delete author (authenticated users only)
    
    Features:
        - Nested serialization: Includes all author's books in response
        - Query optimization: Uses prefetch_related('books')
        - Cascade delete: Deleting author also deletes their books
    
    Permissions:
        - GET: Open to all users
        - PUT/PATCH/DELETE: Authenticated users only
    
    Important Notes:
        - When an author is deleted, all their books are cascade deleted
          due to on_delete=models.CASCADE in the Book model
    
    Example Requests:
        GET /api/authors/1/
        PUT /api/authors/1/ (with authentication)
        PATCH /api/authors/1/ (with authentication)
        DELETE /api/authors/1/ (with authentication - cascades to books)
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
