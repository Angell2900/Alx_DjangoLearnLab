# Creating a Book Entry

To create a new book entry, use the Django shell:

```python
# Start the Django shell
python manage.py shell

# Import the Book model
from bookshelf.models import Book

# Create a new book instance
book = Book(
    title="1984",
    author="George Orwell",
    publication_year=1949
)

# Save the book to the database
book.save()

# Verify the book was created
book_check = Book.objects.get(title="1984")
print(f"Created book: {book_check.title} by {book_check.author} ({book_check.publication_year})")
```

Expected output:
```
Created book: 1984 by George Orwell (1949)
```
