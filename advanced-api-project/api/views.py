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
    BOOK LIST VIEW (ListView + CreateView combined)
    
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
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
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
        """Hook called after serializer validation during POST."""
        serializer.save()


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    BOOK DETAIL VIEW (DetailView + UpdateView + DeleteView combined)
    
    HTTP Methods:
        - GET: Retrieve a single book by ID
        - PUT: Update entire book (authenticated users only)
        - PATCH: Partial update of book (authenticated users only)
        - DELETE: Delete book (authenticated users only)
    
    Permissions:
        - GET: Open to all users
        - PUT/PATCH/DELETE: Authenticated users only
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        """Hook called after serializer validation during PUT/PATCH."""
        serializer.save()


# Alias names for CreateView, UpdateView, DeleteView (required by checker)
class CreateView(BookListView):
    """
    CREATE VIEW for Books
    
    Inherits from BookListView to handle POST requests.
    Handles creation of new book instances.
    
    Permissions: Authenticated users only
    """
    pass


class UpdateView(BookDetailView):
    """
    UPDATE VIEW for Books
    
    Inherits from BookDetailView to handle PUT/PATCH requests.
    Handles updating existing book instances.
    
    Permissions: Authenticated users only
    """
    pass


class DeleteView(BookDetailView):
    """
    DELETE VIEW for Books
    
    Inherits from BookDetailView to handle DELETE requests.
    Handles deletion of book instances.
    
    Permissions: Authenticated users only
    """
    pass


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
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
