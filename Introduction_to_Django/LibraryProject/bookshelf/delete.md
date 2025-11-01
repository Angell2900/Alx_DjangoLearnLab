# Deleting a Book

```python
from bookshelf.models import Book

# Get and delete the book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Verify deletion
remaining_books = Book.objects.all()
print("Remaining books:", remaining_books)
```
