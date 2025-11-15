# Retrieving Books

```python
from bookshelf.models import Book

# Get all books
all_books = Book.objects.all()
print("All books:", all_books)

# Get specific book
book = Book.objects.get(title="1984")
print(f"Found: {book.title} by {book.author} ({book.publication_year})")
```
