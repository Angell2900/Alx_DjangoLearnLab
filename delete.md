```markdown
# Delete a Book

```python
from libraryapp.models import Book

# Get the book we want to delete
book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete it
book.delete()

# Check all books
Book.objects.all()