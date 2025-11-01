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
````

# Create the directory "Introduction_to_Django"

You can create the required directory and optionally initialize a Django project/app inside it.

Terminal commands (from your project root):
```bash
# go to project root (adjust if needed)
cd /Users/angelibzw/Developer/alx_prodevbackend/Alx_DjangoLearnLab

# create the directory
mkdir Introduction_to_Django

# add a README so the folder is visible in git, or a .gitkeep if empty
echo "# Introduction to Django" > Introduction_to_Django/README.md
touch Introduction_to_Django/.gitkeep

# Option A — start a Django project inside the new folder:
cd Introduction_to_Django
django-admin startproject mysite .

# Option B — create a Django app inside the new folder:
# (from inside Introduction_to_Django)
django-admin startapp example_app

# Move existing assignment files into the new folder (example)
# mv /path/to/file Introduction_to_Django/

# Add & commit changes
cd /Users/angelibzw/Developer/alx_prodevbackend/Alx_DjangoLearnLab
git add Introduction_to_Django
git commit -m "Add Introduction_to_Django directory and starter files"
```
```