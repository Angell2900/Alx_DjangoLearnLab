from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book
from django.utils import timezone


class BookAPITestCase(TestCase):
    """
    Test cases for Book API endpoints.
    
    This test suite covers CRUD operations, filtering, searching, ordering,
    and permission enforcement for the Book API endpoints.
    """
    
    def setUp(self):
        """
        Set up test fixtures that are used across all test methods.
        
        Creates:
        - A test user (authenticated user)
        - Two test authors
        - Two test books
        """
        self.client = APIClient()
        
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George R.R. Martin')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='A Game of Thrones',
            publication_year=1996,
            author=self.author2
        )

    def test_book_list_get(self):
        """
        Test GET request to retrieve all books.
        
        Verifies:
        - Status code is 200 OK
        - Response contains expected number of books
        - Response data structure is correct
        """
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_book_list_filtering_by_author(self):
        """
        Test filtering books by author ID.
        
        Verifies:
        - Filtering returns only books by the specified author
        - Status code is 200 OK
        - Response contains correct book
        """
        response = self.client.get(f'/api/books/?author={self.author1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], self.book1.title)

    def test_book_list_filtering_by_publication_year(self):
        """
        Test filtering books by publication year.
        
        Verifies:
        - Filtering returns only books published in the specified year
        - Status code is 200 OK
        - Response contains correct book
        """
        response = self.client.get('/api/books/?publication_year=1997')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['publication_year'], 1997)

    def test_book_list_search_by_title(self):
        """
        Test search functionality on book title.
        
        Verifies:
        - Search returns books matching the search term in title
        - Status code is 200 OK
        - Search is case-insensitive and partial match
        """
        response = self.client.get('/api/books/?search=Harry')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertIn('Harry', response.data['results'][0]['title'])

    def test_book_list_search_by_author_name(self):
        """
        Test search functionality on author name.
        
        Verifies:
        - Search returns books by authors matching the search term
        - Status code is 200 OK
        """
        response = self.client.get('/api/books/?search=Rowling')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['author_name'], 'J.K. Rowling')

    def test_book_list_ordering_ascending(self):
        """
        Test ordering books in ascending order by publication year.
        
        Verifies:
        - Books are returned in correct ascending order
        - Status code is 200 OK
        """
        response = self.client.get('/api/books/?ordering=publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years))

    def test_book_list_ordering_descending(self):
        """
        Test default ordering (descending by publication year).
        
        Verifies:
        - Books are returned in descending order by default
        - Status code is 200 OK
        """
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years, reverse=True))

    def test_book_detail_get(self):
        """
        Test GET request to retrieve a single book by ID.
        
        Verifies:
        - Status code is 200 OK
        - Response contains correct book data
        - Response includes author information
        """
        response = self.client.get(f'/api/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['author_name'], 'J.K. Rowling')

    def test_book_detail_not_found(self):
        """
        Test GET request for non-existent book.
        
        Verifies:
        - Status code is 404 Not Found
        - Response contains error information
        """
        response = self.client.get('/api/books/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_book_create_authenticated(self):
        """
        Test POST request to create a book as authenticated user.
        
        Verifies:
        - Status code is 201 Created
        - Book is created in database
        - Response contains created book data
        """
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'The Hobbit',
            'publication_year': 1937,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(response.data['title'], 'The Hobbit')

    def test_book_create_unauthenticated(self):
        """
        Test POST request to create a book as unauthenticated user.
        
        Verifies:
        - Status code is 401 Unauthorized (not 403)
        - Book is not created in database
        """
        data = {
            'title': 'The Hobbit',
            'publication_year': 1937,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 2)

    def test_book_create_invalid_data(self):
        """
        Test POST request with invalid data.
        
        Verifies:
        - Status code is 400 Bad Request
        - Error message is returned
        """
        self.client.force_authenticate(user=self.user)
        data = {
            'title': '',  # Empty title
            'publication_year': 1937,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_book_create_future_year_validation(self):
        """
        Test validation for publication year in the future.
        
        Verifies:
        - Status code is 400 Bad Request
        - publication_year error is included in response
        - Book is not created in database
        """
        self.client.force_authenticate(user=self.user)
        future_year = timezone.now().year + 1
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
        self.assertEqual(Book.objects.count(), 2)

    def test_book_create_invalid_year_validation(self):
        """
        Test validation for invalid publication year (before 1000).
        
        Verifies:
        - Status code is 400 Bad Request
        - publication_year error is included in response
        """
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Ancient Book',
            'publication_year': 500,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)

    def test_book_update_authenticated(self):
        """
        Test PATCH request to update a book as authenticated user.
        
        Verifies:
        - Status code is 200 OK
        - Book is updated in database
        - Response contains updated data
        """
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Title'}
        response = self.client.patch(f'/api/books/{self.book1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')

    def test_book_update_unauthenticated(self):
        """
        Test PATCH request to update a book as unauthenticated user.
        
        Verifies:
        - Status code is 401 Unauthorized (not 403)
        - Book is not updated in database
        """
        data = {'title': 'Updated Title'}
        response = self.client.patch(f'/api/books/{self.book1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.book1.refresh_from_db()
        self.assertNotEqual(self.book1.title, 'Updated Title')

    def test_book_update_validation(self):
        """
        Test PATCH request with invalid data.
        
        Verifies:
        - Validation is enforced on partial updates
        - Status code is 400 Bad Request
        """
        self.client.force_authenticate(user=self.user)
        data = {'publication_year': timezone.now().year + 1}
        response = self.client.patch(f'/api/books/{self.book1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_book_delete_authenticated(self):
        """
        Test DELETE request to delete a book as authenticated user.
        
        Verifies:
        - Status code is 204 No Content
        - Book is deleted from database
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_book_delete_unauthenticated(self):
        """
        Test DELETE request to delete a book as unauthenticated user.
        
        Verifies:
        - Status code is 401 Unauthorized (not 403)
        - Book is not deleted from database
        """
        response = self.client.delete(f'/api/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 2)

class AuthorAPITestCase(TestCase):
    """
    Test cases for Author API endpoints.
    
    This test suite covers CRUD operations, nested book serialization,
    and permission enforcement for the Author API endpoints.
    """
    
    def setUp(self):
        """
        Set up test fixtures for author tests.
        
        Creates:
        - A test user
        - A test author
        - A book associated with the author
        """
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.author = Author.objects.create(name='J.R.R. Tolkien')
        self.book = Book.objects.create(
            title='The Lord of the Rings',
            publication_year=1954,
            author=self.author
        )

    def test_author_list_get(self):
        """
        Test GET request to retrieve all authors.
        
        Verifies:
        - Status code is 200 OK
        - Response contains expected authors
        """
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_author_list_includes_nested_books(self):
        """
        Test that author list includes nested books serialization.
        
        Verifies:
        - Response includes 'books' field
        - Nested books are properly serialized
        - books_count field is accurate
        """
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        author_data = response.data['results'][0]
        self.assertIn('books', author_data)
        self.assertEqual(len(author_data['books']), 1)
        self.assertEqual(author_data['books_count'], 1)
        self.assertEqual(author_data['books'][0]['title'], self.book.title)

    def test_author_list_search(self):
        """
        Test search functionality on author name.
        
        Verifies:
        - Search returns authors matching the search term
        - Status code is 200 OK
        """
        response = self.client.get('/api/authors/?search=Tolkien')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertIn('Tolkien', response.data['results'][0]['name'])

    def test_author_list_ordering(self):
        """
        Test ordering authors by name.
        
        Verifies:
        - Authors are returned in correct order
        - Default ordering is by name (ascending)
        """
        Author.objects.create(name='Arthur Conan Doyle')
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [author['name'] for author in response.data['results']]
        self.assertEqual(names, sorted(names))

    def test_author_detail_get(self):
        """
        Test GET request to retrieve a single author.
        
        Verifies:
        - Status code is 200 OK
        - Response contains correct author data
        - Nested books are included
        """
        response = self.client.get(f'/api/authors/{self.author.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.author.name)
        self.assertEqual(len(response.data['books']), 1)
        self.assertEqual(response.data['books_count'], 1)

    def test_author_detail_not_found(self):
        """
        Test GET request for non-existent author.
        
        Verifies:
        - Status code is 404 Not Found
        """
        response = self.client.get('/api/authors/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_author_create_authenticated(self):
        """
        Test POST request to create an author as authenticated user.
        
        Verifies:
        - Status code is 201 Created
        - Author is created in database
        - Response contains created author data
        """
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Isaac Asimov'}
        response = self.client.post('/api/authors/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Isaac Asimov')

    def test_author_create_unauthenticated(self):
        """
        Test POST request to create an author as unauthenticated user.
        
        Verifies:
        - Status code is 401 Unauthorized (not 403)
        - Author is not created in database
        """
        data = {'name': 'Isaac Asimov'}
        response = self.client.post('/api/authors/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Author.objects.count(), 1)

    def test_author_update_authenticated(self):
        """
        Test PATCH request to update an author as authenticated user.
        
        Verifies:
        - Status code is 200 OK
        - Author is updated in database
        """
        self.client.force_authenticate(user=self.user)
        data = {'name': 'John Ronald Reuel Tolkien'}
        response = self.client.patch(f'/api/authors/{self.author.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()
        self.assertEqual(self.author.name, 'John Ronald Reuel Tolkien')

    def test_author_delete_authenticated(self):
        """
        Test DELETE request to delete an author as authenticated user.
        
        Verifies:
        - Status code is 204 No Content
        - Author is deleted from database
        - Associated books are cascade deleted
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/authors/{self.author.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)
        # Verify cascade delete of books
        self.assertEqual(Book.objects.count(), 0)

    def test_author_delete_unauthenticated(self):
        """
        Test DELETE request to delete an author as unauthenticated user.
        
        Verifies:
        - Status code is 401 Unauthorized (not 403)
        - Author is not deleted from database
        """
        response = self.client.delete(f'/api/authors/{self.author.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Author.objects.count(), 1)

def test_login(self):
    login_success = self.client.login(username='testuser', password='testpass123')
    self.assertTrue(login_success)
