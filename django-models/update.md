# Update a Book

```python
from bookshelf.models import Book

# Get and update the book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Verify update
updated_book = Book.objects.get(id=book.id)
print(f"Updated title: {updated_book.title}")
```
