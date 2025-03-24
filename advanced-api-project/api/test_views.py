from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import User
from .models import Author, Book
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView

class BookListViewTests(TestCase):

    def setUp(self):
        """Set up test data before each test"""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(title="Harry Potter", publication_year=1997, author=self.author)
        self.book2 = Book.objects.create(title="The Hobbit", publication_year=1937, author=self.author)
        self.factory = APIRequestFactory()

    def test_list_books(self):
        """Test retrieving the list of books"""
        # Create a GET request to the BookListView endpoint
        request = self.factory.get('/api/books/')

        # Force authentication for the request
        force_authenticate(request, user=self.user)

        # Initialize the view
        view = BookListView.as_view()

        # Call the view with the request
        response = view(request)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check if both books are included in the response data
        self.assertEqual(len(response.data), 2)

        # Check if the titles of the books are correct
        self.assertEqual(response.data[0]['title'], "Harry Potter")
        self.assertEqual(response.data[1]['title'], "The Hobbit")

    def test_list_books_unauthenticated(self):
        """Test that unauthenticated users can access the book list"""
        # Create a GET request to the BookListView endpoint
        request = self.factory.get('/api/books/')

        # No authentication here (unauthenticated user)
        view = BookListView.as_view()

        # Call the view with the request
        response = view(request)

        # Check if the response status code is 200 OK (since we allowed public access to the list view)
        self.assertEqual(response.status_code, 200)

        # Check if both books are included in the response data
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], "Harry Potter")
        self.assertEqual(response.data[1]['title'], "The Hobbit")

class BookDetailViewTests(TestCase):

    def setUp(self):
        """Set up test data before each test"""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(title="Harry Potter", publication_year=1997, author=self.author)
        self.factory = APIRequestFactory()

    def test_retrieve_book(self):
        """Test retrieving a single book"""
        request = self.factory.get(f'/api/books/{self.book.id}/')
        force_authenticate(request, user=self.user)
        view = BookDetailView.as_view()
        response = view(request, pk=self.book.id)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check if the returned data is correct
        self.assertEqual(response.data['title'], "Harry Potter")
        self.assertEqual(response.data['author'], self.author.pk)

    def test_retrieve_non_existent_book(self):
        """Test that retrieving a non-existent book returns a 404"""
        request = self.factory.get('/api/books/999/')
        force_authenticate(request, user=self.user)
        view = BookDetailView.as_view()
        response = view(request, pk=999)

        # Check if the response status code is 404 Not Found
        self.assertEqual(response.status_code, 404)


class BookCreateViewTests(TestCase):

    def setUp(self):
        """Set up test data before each test"""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(name="J.K. Rowling")
        self.factory = APIRequestFactory()

    def test_create_book(self):
        """Test creating a new book"""
        data = {
            "title": "New Book",
            "publication_year": 2023,
            "author": self.author.id
        }
        request = self.factory.post('/api/books/create/', data, format='json')
        force_authenticate(request, user=self.user)
        view = BookCreateView.as_view()
        response = view(request)

        # Check if the response status code is 201 Created
        self.assertEqual(response.status_code, 201)

        # Check if the book is created and in the response
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(response.data['title'], "New Book")

    def test_create_book_unauthenticated(self):
        """Test that an unauthenticated user cannot create a book"""
        data = {
            "title": "Unauthorized Book",
            "publication_year": 2025,
            "author": self.author.id
        }
        request = self.factory.post('/api/books/create/', data, format='json')
        # Don't authenticate for an unauthenticated user
        view = BookCreateView.as_view()
        response = view(request)

        # Check if the response status code is 401 Unauthorized
        self.assertEqual(response.status_code, 401)

class BookUpdateViewTests(TestCase):

    def setUp(self):
        """Set up test data before each test"""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(title="Harry Potter", publication_year=1997, author=self.author)
        self.factory = APIRequestFactory()

    def test_update_book(self):
        """Test updating an existing book"""
        data = {
            "title": "Updated Harry Potter",
            "publication_year": 2000,
            "author": self.author.id
        }
        request = self.factory.put(f'/api/books/update/{self.book.id}/', data, format='json')
        force_authenticate(request, user=self.user)
        view = BookUpdateView.as_view()
        response = view(request, pk=self.book.id)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check if the book's title and year were updated
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Harry Potter")
        self.assertEqual(self.book.publication_year, 2000)

    def test_update_book_unauthenticated(self):
        """Test that an unauthenticated user cannot update a book"""
        data = {
            "title": "Unauthorized Update",
            "publication_year": 2025,
            "author": self.author.id
        }
        request = self.factory.put(f'/api/books/update/{self.book.id}/', data, format='json')
        view = BookUpdateView.as_view()
        response = view(request, pk=self.book.id)

        # Check if the response status code is 401 Unauthorized
        self.assertEqual(response.status_code, 401)


class BookDeleteViewTests(TestCase):

    def setUp(self):
        """Set up test data before each test"""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(title="Harry Potter", publication_year=1997, author=self.author)
        self.factory = APIRequestFactory()

    def test_delete_book(self):
        """Test deleting a book"""
        request = self.factory.delete(f'/api/books/delete/{self.book.id}/')
        force_authenticate(request, user=self.user)
        view = BookDeleteView.as_view()
        response = view(request, pk=self.book.id)

        # Check if the response status code is 204 No Content (successful delete)
        self.assertEqual(response.status_code, 204)

        # Check if the book is removed from the database
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_delete_book_unauthenticated(self):
        """Test that an unauthenticated user cannot delete a book"""
        request = self.factory.delete(f'/api/books/delete/{self.book.id}/')
        view = BookDeleteView.as_view()
        response = view(request, pk=self.book.id)

        # Check if the response status code is 401 Unauthorized
        self.assertEqual(response.status_code, 401)

