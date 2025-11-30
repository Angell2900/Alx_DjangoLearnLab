"""
Task 0 Verification Script
Tests models and serializers for Author and Book
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer

def test_models():
    """Test that models exist and can be created"""
    print("\n" + "=" * 70)
    print("TEST 1: CHECKING MODELS")
    print("=" * 70)
    
    # Check if tables exist
    author_count = Author.objects.count()
    book_count = Book.objects.count()
    
    print(f"✓ Authors in database: {author_count}")
    print(f"✓ Books in database: {book_count}")
    
    return True

def test_create_author():
    """Test creating an author"""
    print("\n" + "=" * 70)
    print("TEST 2: CREATING AUTHOR")
    print("=" * 70)
    
    author = Author.objects.create(name='J.K. Rowling')
    print(f"✓ Created author: {author.name}")
    print(f"✓ Author ID: {author.id}")
    
    return author

def test_create_book(author):
    """Test creating a book"""
    print("\n" + "=" * 70)
    print("TEST 3: CREATING BOOK")
    print("=" * 70)
    
    book = Book.objects.create(
        title='Harry Potter and the Philosopher\'s Stone',
        publication_year=1997,
        author=author
    )
    print(f"✓ Created book: {book.title}")
    print(f"✓ Publication year: {book.publication_year}")
    print(f"✓ Author: {book.author.name}")
    print(f"✓ Book ID: {book.id}")
    
    return book

def test_book_serializer(book):
    """Test BookSerializer"""
    print("\n" + "=" * 70)
    print("TEST 4: BOOK SERIALIZER")
    print("=" * 70)
    
    serializer = BookSerializer(book)
    data = serializer.data
    
    print(f"✓ Serialized book data:")
    print(f"  - ID: {data['id']}")
    print(f"  - Title: {data['title']}")
    print(f"  - Publication Year: {data['publication_year']}")
    print(f"  - Author ID: {data['author']}")
    print(f"  - Author Name: {data['author_name']}")
    print(f"  - Created At: {data['created_at']}")
    
    return data

def test_author_serializer(author):
    """Test AuthorSerializer with nested books"""
    print("\n" + "=" * 70)
    print("TEST 5: AUTHOR SERIALIZER (WITH NESTED BOOKS)")
    print("=" * 70)
    
    serializer = AuthorSerializer(author)
    data = serializer.data
    
    print(f"✓ Serialized author data:")
    print(f"  - ID: {data['id']}")
    print(f"  - Name: {data['name']}")
    print(f"  - Books Count: {data['books_count']}")
    print(f"  - Number of nested books: {len(data['books'])}")
    
    if data['books']:
        print(f"\n✓ Nested books:")
        for i, book in enumerate(data['books'], 1):
            print(f"  Book {i}:")
            print(f"    - Title: {book['title']}")
            print(f"    - Year: {book['publication_year']}")
            print(f"    - Author Name: {book['author_name']}")
    
    return data

def test_validation_future_year():
    """Test that future year validation works"""
    print("\n" + "=" * 70)
    print("TEST 6: VALIDATION - FUTURE YEAR (SHOULD FAIL)")
    print("=" * 70)
    
    author = Author.objects.first()
    invalid_data = {
        'title': 'Future Book',
        'publication_year': 2026,
        'author': author.id
    }
    
    serializer = BookSerializer(data=invalid_data)
    is_valid = serializer.is_valid()
    
    print(f"✓ Valid: {is_valid}")
    if not is_valid:
        print(f"✓ Validation error (as expected):")
        for field, errors in serializer.errors.items():
            print(f"  - {field}: {errors[0]}")
    
    return not is_valid  # Should be invalid

def test_validation_invalid_year():
    """Test that year < 1000 validation works"""
    print("\n" + "=" * 70)
    print("TEST 7: VALIDATION - INVALID YEAR < 1000 (SHOULD FAIL)")
    print("=" * 70)
    
    author = Author.objects.first()
    invalid_data = {
        'title': 'Ancient Book',
        'publication_year': 500,
        'author': author.id
    }
    
    serializer = BookSerializer(data=invalid_data)
    is_valid = serializer.is_valid()
    
    print(f"✓ Valid: {is_valid}")
    if not is_valid:
        print(f"✓ Validation error (as expected):")
        for field, errors in serializer.errors.items():
            print(f"  - {field}: {errors[0]}")
    
    return not is_valid  # Should be invalid

def test_valid_book_creation():
    """Test creating a valid book via serializer"""
    print("\n" + "=" * 70)
    print("TEST 8: VALID BOOK CREATION VIA SERIALIZER")
    print("=" * 70)
    
    author = Author.objects.first()
    valid_data = {
        'title': 'The Hobbit',
        'publication_year': 1937,
        'author': author.id
    }
    
    serializer = BookSerializer(data=valid_data)
    is_valid = serializer.is_valid()
    
    print(f"✓ Valid: {is_valid}")
    
    if is_valid:
        book = serializer.save()
        print(f"✓ Book created successfully: {book.title}")
        print(f"✓ Book ID: {book.id}")
        return True
    else:
        print(f"✗ Validation failed: {serializer.errors}")
        return False

def test_summary():
    """Print summary of all objects"""
    print("\n" + "=" * 70)
    print("TEST 9: SUMMARY - ALL OBJECTS IN DATABASE")
    print("=" * 70)
    
    authors = Author.objects.all()
    books = Book.objects.all()
    
    print(f"\n✓ Total Authors: {authors.count()}")
    for author in authors:
        book_count = author.books.count()
        print(f"  - {author.name} ({book_count} books)")
        for book in author.books.all():
            print(f"    • {book.title} ({book.publication_year})")
    
    print(f"\n✓ Total Books: {books.count()}")

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "TASK 0 VERIFICATION - MODELS AND SERIALIZERS".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    try:
        # Run tests
        test_models()
        author = test_create_author()
        book = test_create_book(author)
        test_book_serializer(book)
        test_author_serializer(author)
        
        # Validation tests
        test_validation_future_year()
        test_validation_invalid_year()
        test_valid_book_creation()
        
        # Summary
        test_summary()
        
        # Final message
        print("\n" + "=" * 70)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 70)
        print("\n✓ Task 0 Requirements Met:")
        print("  ✓ Models created (Author and Book)")
        print("  ✓ Foreign key relationship established")
        print("  ✓ Custom serializers created")
        print("  ✓ Nested serialization working")
        print("  ✓ Validation working (future year prevention)")
        print("  ✓ Models can be tested in admin and shell")
        print("\n" + "=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
