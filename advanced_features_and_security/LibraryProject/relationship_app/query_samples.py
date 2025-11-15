from relationship_app.models import Book, Author, Library, Librarian

print("\n--- LIST ALL BOOKS IN A LIBRARY ---")
library_name = "Central Library"  
try:
    library = Library.objects.get(name=library_name)   
    books_in_library = library.books.all()             
    print(f"Books in {library_name}:", books_in_library)
except Library.DoesNotExist:
    print(f"No library named {library_name} found.")


print("\n--- QUERY ALL BOOKS BY A SPECIFIC AUTHOR ---")
author_name = "J.K. Rowling"
try:
    author = Author.objects.get(name=author_name)      
    books_by_author = Book.objects.filter(author=author)  
    print(f"Books by {author_name}:", books_by_author)
except Author.DoesNotExist:
    print(f"No author named {author_name} found.")


print("\n--- RETRIEVE THE LIBRARIAN FOR A LIBRARY ---")
try:
    librarian = Librarian.objects.get(library=library)   
    print(f"Librarian for {library_name}:", librarian)
except:
    print(f"No librarian assigned to {library_name}.")
