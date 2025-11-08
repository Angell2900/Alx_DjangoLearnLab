# Retrieve a Book

```python
from bookshelf.models import Book

# Get the book
book = Book.objects.get(title="1984")

# Display all attributes
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```
