```markdown
# Update a Book

```python
from libraryapp.models import Book

# Get the book we want to update
book = Book.objects.get(title="1984")

# Change the title
book.title = "Nineteen Eighty-Four"

# Save changes
book.save()

# Check updated book
book