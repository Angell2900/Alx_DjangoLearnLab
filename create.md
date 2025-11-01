# Create a Book

```python
from libraryapp.models import Book

# Create a new book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Check the book
book
