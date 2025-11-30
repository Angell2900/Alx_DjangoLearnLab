from rest_framework import serializers
from django.utils import timezone
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    This serializer handles the serialization and deserialization of Book instances.
    It includes the book's basic information and the author's name for easier access
    without requiring separate API calls.
    
    Fields:
        - id: The book's unique identifier (read-only)
        - title: The book's title (string, max 255 characters)
        - publication_year: The year the book was published (integer)
        - author: The foreign key ID of the author (required for creation)
        - author_name: The author's name (read-only, sourced from author.name)
        - created_at: The creation timestamp (read-only)
    
    Validation:
        - publication_year: Custom validator to ensure the year is not in the future
          and is a valid historical year (1000 or later)
    
    Nested Relationships:
        - The author is represented as an ID for creation/updates, but author_name 
          provides the actual author name for convenient client-side access without 
          requiring separate queries to the Author model.
    
    Usage Example:
        # Serializing a Book instance
        book = Book.objects.first()
        serializer = BookSerializer(book)
        print(serializer.data)
        
        # Creating a new Book
        data = {
            'title': 'The Hobbit',
            'publication_year': 1937,
            'author': 1
        }
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
    """
    # This field reads the related author's name without requiring a nested serializer
    # It makes the API response more user-friendly by including the author's name
    author_name = serializers.CharField(
        source='author.name',
        read_only=True,
        help_text="The name of the book's author"
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author', 'author_name', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_publication_year(self, value):
        """
        Validate that publication_year is not in the future.
        
        This custom validator is called automatically by DRF during deserialization.
        It ensures that:
        1. The publication year is not in the future
        2. The publication year is a valid historical year (1000 or later)
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If the year is in the future or invalid
        
        Examples:
            - Year 2025 (future): Raises ValidationError
            - Year 500 (too old): Raises ValidationError
            - Year 1997: Valid, returns 1997
        """
        current_year = timezone.now().year
        
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        
        if value < 1000:
            raise serializers.ValidationError(
                "Publication year must be a valid year (1000 or later)."
            )
        
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    
    This serializer handles the serialization and deserialization of Author instances.
    It includes nested Book serialization to display all books by an author in a single 
    request, providing a complete view of an author and their bibliography.
    
    Fields:
        - id: The author's unique identifier (read-only)
        - name: The author's name (string, max 255 characters)
        - books: Nested serialization of all books by this author (read-only)
        - books_count: The total number of books by this author (read-only, computed field)
        - created_at: The creation timestamp (read-only)
    
    Nested Relationships:
        - books: Uses BookSerializer to represent all related books in a nested structure.
          This allows clients to retrieve author information along with all their books
          in a single API call, improving efficiency and reducing N+1 query problems
          when using prefetch_related() in views.
    
    Computed Fields:
        - books_count: Dynamically calculates the number of books for this author
          using the get_books_count() method. Useful for quick statistics.
    
    Usage Example:
        # Serializing an Author with nested books
        author = Author.objects.first()
        serializer = AuthorSerializer(author)
        print(serializer.data)
        # Output:
        # {
        #     'id': 1,
        #     'name': 'J.K. Rowling',
        #     'books': [
        #         {'id': 1, 'title': 'Harry Potter...', 'publication_year': 1997, ...},
        #         {'id': 2, 'title': 'Harry Potter...', 'publication_year': 1998, ...}
        #     ],
        #     'books_count': 2,
        #     'created_at': '2024-01-15T10:30:00Z'
        # }
        
        # Creating a new Author
        data = {'name': 'George R.R. Martin'}
        serializer = AuthorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
    """
    # Nested serializer that includes all books related to this author
    # many=True indicates this is a one-to-many relationship
    # read_only=True because we don't accept book data in POST requests for authors
    books = BookSerializer(many=True, read_only=True)
    
    # Custom field that calculates the number of books dynamically
    books_count = serializers.SerializerMethodField(
        help_text="Total number of books by this author"
    )

    class Meta:
        model = Author
        fields = ['id', 'name', 'books', 'books_count', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_books_count(self, obj):
        """
        Calculate the total count of books for an author.
        
        This method is a SerializerMethodField that is called during serialization
        to dynamically compute the number of books written by the author.
        
        Note: This uses obj.books.count() which generates a SQL COUNT query.
        For better performance with large datasets, consider adding books_count
        as a field in the Author model or using annotate() in the view's queryset.
        
        Args:
            obj (Author): The Author instance being serialized
            
        Returns:
            int: The total number of books written by this author
        
        Example:
            For an author with 7 books:
            - Input: Author object for J.K. Rowling
            - Output: 7
        """
        return obj.books.count()
