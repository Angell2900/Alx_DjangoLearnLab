from relationship_app.models import Book, Author, Library, Librarian


books = Book.objects.all()
print("All Books:", books)

try:
    harry = Book.objects.get(title="Harry Potter")
    print("Specific Book:", harry)
except Book.DoesNotExist:
    print("Harry Potter is not in the database yet.")

new_author = Author.objects.create(name="Chinua Achebe")
print("New Author Created:", new_author)

new_book = Book.objects.create(title="Things Fall Apart", author=new_author)
print("New Book Created:", new_book)

authors = Author.objects.all()
print("All Authors:", authors)

libraries = Library.objects.all()
print("Libraries:", libraries)

librarians = Librarian.objects.all()
print("Librarians:", librarians)
