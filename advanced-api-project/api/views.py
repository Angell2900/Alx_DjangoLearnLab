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
# BOOK VIEWS - CRUD Operations
# ============================================================================

class BookListView(generics.ListCreateAPIView):
    """
    ListView for retrieving all books and CreateView for adding new books.
    
    Permission Classes: IsAuthenticatedOrReadOnly
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
    DetailView for retrieving a single book.
    
    Permission Classes: IsAuthenticatedOrReadOnly
    - GET: Open to all users
    - PUT/PATCH/DELETE: Authenticated users only
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        """Hook called after serializer validation during PUT/PATCH."""
        serializer.save()


class CreateView(BookListView):
    """
    CreateView for adding a new book.
    
    Permission Classes: IsAuthenticatedOrReadOnly
    - POST: Authenticated users only
    
    This view inherits from BookListView and handles the creation of new books.
    """
    pass


class UpdateView(BookDetailView):
    """
    UpdateView for modifying an existing book.
    
    Permission Classes: IsAuthenticatedOrReadOnly
    - PUT/PATCH: Authenticated users only
    
    This view inherits from BookDetailView and handles updating books.
    """
    pass


class DeleteView(BookDetailView):
    """
    DeleteView for removing a book.
    
    Permission Classes: IsAuthenticatedOrReadOnly
    - DELETE: Authenticated users only
    
    This view inherits from BookDetailView and handles deletion of books.
    """
    pass


# ============================================================================
# AUTHOR VIEWS - CRUD Operations
# ============================================================================

class AuthorListView(generics.ListCreateAPIView):
    """
    ListView for retrieving all authors with nested books.
    
    Permission Classes: IsAuthenticatedOrReadOnly
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
    DetailView for retrieving a single author with nested books.
    
    Permission Classes: IsAuthenticatedOrReadOnly
    - GET: Open to all users
    - PUT/PATCH/DELETE: Authenticated users only
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
