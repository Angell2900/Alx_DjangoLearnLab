from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Django admin configuration for the Author model.
    
    Allows admins to:
    - View all authors
    - Create new authors
    - Edit author information
    - Delete authors
    - Search by author name
    - Filter by creation date
    """
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = (
        ('Author Information', {
            'fields': ('name',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Django admin configuration for the Book model.
    
    Allows admins to:
    - View all books
    - Create new books
    - Edit book information
    - Delete books
    - Search by title or author
    - Filter by publication year and author
    """
    list_display = ['title', 'author', 'publication_year', 'created_at']
    list_filter = ['publication_year', 'author', 'created_at']
    search_fields = ['title', 'author__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-publication_year', 'title']
    
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author', 'publication_year')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
