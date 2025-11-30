from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from django_filters import rest_framework

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
    ListView for retrieving all books and CreateView for adding new books.
    
    Features:
        - Filtering: By author, publication_year, title
        - Searching: On title and author name (SearchFilter)
        - Ordering: By title, publication_year (OrderingFilter)
    
    Permission Classes: IsAuthenticatedOrReadOnly
    - GET: Open to all users
    - POST: Authenticated users only
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Configure filtering backend (DjangoFilterBackend)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Configure fields that can be filtered
    filterset_fields = ['author', 'publication_year', 'title']
    
    # Configure SearchFilter - search on title and author name
    search_fields = ['title', 'author__name']
    
    # Configure OrderingFilter - order by title and publication_year
    ordering_fields = ['title', 'publication_year', 'created_at']
    ordering = ['-publication_year', 'title']

    def perform_create(self, serializer):
        """Hook called after serializer validation during POST."""
        serializer.save()


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    DetailView for retrieving a single book.
    
    Permission Classes: IsAuthenticatedOrReadOnly
    - GET: Open to all users
    - PUT/PATCH/DELETE: Authenticated users only
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        """Hook called after serializer validation during PUT/PATCH."""
        serializer.save()


class CreateView(BookListView):
    """
    CreateView for adding a new book.
    
    Permission Classes: IsAuthenticated
    - POST: Authenticated users only
    
    This view inherits from BookListView and handles the creation of new books.
    Includes filtering, searching, and ordering capabilities inherited from parent.
    """
    permission_classes = [IsAuthenticated]


class UpdateView(BookDetailView):
    """
    UpdateView for modifying an existing book.
    
    Permission Classes: IsAuthenticated
    - PUT/PATCH: Authenticated users only
    
    This view inherits from BookDetailView and handles updating books.
    """
    permission_classes = [IsAuthenticated]


class DeleteView(BookDetailView):
    """
    DeleteView for removing a book.
    
    Permission Classes: IsAuthenticated
    - DELETE: Authenticated users only
    
    This view inherits from BookDetailView and handles deletion of books.
    """
    permission_classes = [IsAuthenticated]


# ============================================================================
# AUTHOR VIEWS - CRUD Operations
# ============================================================================

class AuthorListView(generics.ListCreateAPIView):
    """
    ListView for retrieving all authors with nested books.
    
    Features:
        - Searching: On author name (SearchFilter)
        - Ordering: By name and creation date (OrderingFilter)
    
    Permission Classes: IsAuthenticatedOrReadOnly
    - GET: Open to all users
    - POST: Authenticated users only
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Configure SearchFilter and OrderingFilter
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
    # Configure SearchFilter - search on author name
    search_fields = ['name']
    
    # Configure OrderingFilter - order by name and created_at
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    DetailView for retrieving a single author with nested books.
    
    Permission Classes: IsAuthenticatedOrReadOnly
    - GET: Open to all users
    - PUT/PATCH/DELETE: Authenticated users only
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
