from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Django admin configuration for Author model.
    
    Features:
        - Display author name, creation date, and update date
        - Search by author name
        - Filter by creation date
    """
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Django admin configuration for Book model.
    
    Features:
        - Display book title, author, publication year, and dates
        - Filter by publication year and author
        - Search by title and author name
        - Make created_at and updated_at read-only
    """
    list_display = ['title', 'author', 'publication_year', 'created_at', 'updated_at']
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
