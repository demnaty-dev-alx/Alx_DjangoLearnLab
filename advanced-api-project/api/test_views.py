from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from .models import Author, Book
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView

class BookListViewTests(APITestCase):

    def setUp(self):
        """Set up test data before each test"""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(title="Harry Potter", publication_year=1997, author=self.author)
        self.book2 = Book.objects.create(title="The Hobbit", publication_year=1937, author=self.author)

    def test_list_books_authenticated(self):
        """Test retrieving the list of books as an authenticated user"""
        self.client.login(user=self.user)
        response = self.client.get('/api/books/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_books_unauthenticated(self):
        """Test retrieving the book list without authentication"""
        response = self.client.get('/api/books/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class BookDetailViewTests(APITestCase):

    def setUp(self):
        """Set up test data before each test"""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(title="Harry Potter", publication_year=1997, author=self.author)

    def test_retrieve_book_authenticated(self):
        """Test retrieving a single book as an authenticated user"""
        self.client.login(user=self.user)
        response = self.client.get(f'/api/books/{self.book.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Harry Potter")
        self.assertEqual(response.data['author'], self.author.id)  # Make sure author serialization is correct

    def test_retrieve_book_unauthenticated(self):
        """Test retrieving a single book without authentication"""
        response = self.client.get(f'/api/books/{self.book.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Harry Potter")

    def test_retrieve_non_existent_book(self):
        """Test that retrieving a non-existent book returns 404"""
        self.client.login(user=self.user)
        response = self.client.get('/api/books/999/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookCreateViewTests(APITestCase):

    def setUp(self):
        """Set up test data before each test"""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(name="J.K. Rowling")

    def test_create_book_authenticated(self):
        """Test creating a book as an authenticated user"""
        self.client.login(user=self.user)
        data = {
            "title": "New Book",
            "publication_year": 2023,
            "author": self.author.id
        }
        response = self.client.post('/api/books/create/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(response.data['title'], "New Book")

    def test_create_book_unauthenticated(self):
        """Test that an unauthenticated user cannot create a book"""
        data = {
            "title": "Unauthorized Book",
            "publication_year": 2025,
            "author": self.author.id
        }
        response = self.client.post('/api/books/create/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookUpdateViewTests(APITestCase):

    def setUp(self):
        """Set up test data before each test"""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(title="Harry Potter", publication_year=1997, author=self.author)

    def test_update_book_authenticated(self):
        """Test updating an existing book as an authenticated user"""
        self.client.login(user=self.user)
        data = {
            "title": "Updated Harry Potter",
            "publication_year": 2000,
            "author": self.author.id
        }
        response = self.client.put(f'/api/books/update/{self.book.id}/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
        response = self.client.put(f'/api/books/update/{self.book.id}/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookDeleteViewTests(APITestCase):

    def setUp(self):
        """Set up test data before each test"""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(title="Harry Potter", publication_year=1997, author=self.author)

    def test_delete_book_authenticated(self):
        """Test deleting a book as an authenticated user"""
        self.client.login(user=self.user)
        response = self.client.delete(f'/api/books/delete/{self.book.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_delete_book_unauthenticated(self):
        """Test that an unauthenticated user cannot delete a book"""
        response = self.client.delete(f'/api/books/delete/{self.book.id}/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
