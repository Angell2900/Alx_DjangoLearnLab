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
    # Book List View (ListView for retrieving all books)
    path('books/', BookListView.as_view(), name='book-list'),
    
    # Book Detail View (DetailView for retrieving a single book by ID)
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # CreateView - for adding a new book
    path('books/create/', CreateView.as_view(), name='book-create'),
    
    # UpdateView - for modifying an existing book
    path('books/<int:pk>/update/', UpdateView.as_view(), name='book-update'),
    
    # DeleteView - for removing a book
    path('books/<int:pk>/delete/', DeleteView.as_view(), name='book-delete'),
    
    # Author List View (ListView for retrieving all authors with nested books)
    path('authors/', AuthorListView.as_view(), name='author-list'),
    
    # Author Detail View (DetailView for retrieving author with books by ID)
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
]
