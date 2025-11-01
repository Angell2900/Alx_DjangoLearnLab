# Creating a Book Entry

```python
from bookshelf.models import Book

# Create a new book using objects.create()
book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)

# Verify the creation
print(f"Created: {book.title} by {book.author}")
```
