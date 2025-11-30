from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Author(models.Model):
    """
    Model representing an Author.
    
    This model stores information about book authors and establishes
    a one-to-many relationship with the Book model.
    
    Fields:
        - name: The author's full name (string, max 255 characters)
        - created_at: Timestamp when the author record was created
        - updated_at: Timestamp when the author record was last updated
    
    Relationships:
        - One-to-Many with Book: An author can have multiple books
          (accessed via the 'books' related name)
    """
    name = models.CharField(
        max_length=255,
        help_text="The author's full name"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Authors"
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Model representing a Book.
    
    This model stores information about books and maintains a many-to-one
    relationship with the Author model. Each book must have an associated author.
    
    Fields:
        - title: The book's title (string, max 255 characters)
        - publication_year: The year the book was published (integer)
        - author: Foreign key to Author model (establishes many-to-one relationship)
        - created_at: Timestamp when the book record was created
        - updated_at: Timestamp when the book record was last updated
    
    Relationships:
        - Many-to-One with Author: Multiple books belong to one author
          (accessed via the 'author' field and related_name 'books' from Author)
    
    Validation:
        - publication_year must not be in the future
        - publication_year must be a reasonable historical value (1000 or later)
    """
    title = models.CharField(
        max_length=255,
        help_text="The title of the book"
    )
    publication_year = models.IntegerField(
        help_text="The year the book was published"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        help_text="The author of the book"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publication_year', 'title']
        verbose_name_plural = "Books"
        indexes = [
            models.Index(fields=['author', 'publication_year']),
            models.Index(fields=['title']),
        ]

    def __str__(self):
        return f"{self.title} by {self.author.name}"

    def clean(self):
        """
        Validate the book instance.
        Ensures publication_year is not in the future.
        """
        current_year = timezone.now().year
        if self.publication_year > current_year:
            raise ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        if self.publication_year < 1000:
            raise ValidationError(
                "Publication year must be a valid year (1000 or later)."
            )