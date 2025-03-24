from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Author, Book

class BookListViewTests(APITestCase):

    def setUp(self):
        """Set up test data before each test"""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book1 = Book.objects.create(title="Harry Potter", publication_year=1997, author=self.author)
        self.book2 = Book.objects.create(title="The Hobbit", publication_year=1937, author=self.author)

    def test_list_books_authenticated(self):
        """Test retrieving the list of books as an authenticated user"""
        self.client.login(username='testuser', password='testpass')  # Login the user
        response = self.client.get(reverse('book-list'))  # Use reverse() for URLs

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], "Harry Potter")

    def test_list_books_unauthenticated(self):
        """Test that unauthenticated users can access the book list"""
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class BookDetailViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(title="Harry Potter", publication_year=1997, author=self.author)

    def test_retrieve_book_authenticated(self):
        """Test retrieving a single book with authentication"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('book-detail', kwargs={'pk': self.book.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Harry Potter")

    def test_retrieve_book_unauthenticated(self):
        """Test retrieving a book without authentication (should still work if public)"""
        response = self.client.get(reverse('book-detail', kwargs={'pk': self.book.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class BookCreateViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(name="J.K. Rowling")

    def test_create_book_authenticated(self):
        """Test creating a new book as an authenticated user"""
        self.client.login(username='testuser', password='testpass')
        data = {"title": "New Book", "publication_year": 2023, "author": self.author.pk}
        response = self.client.post(reverse('book-create'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(response.data['title'], "New Book")

    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create a book"""
        data = {"title": "Unauthorized Book", "publication_year": 2025, "author": self.author.pk}
        response = self.client.post(reverse('book-create'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class BookUpdateViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(title="Harry Potter", publication_year=1997, author=self.author)

    def test_update_book_authenticated(self):
        """Test updating a book as an authenticated user"""
        self.client.login(username='testuser', password='testpass')
        data = {"title": "Updated Harry Potter", "publication_year": 2000, "author": self.author.pk}
        response = self.client.put(reverse('book-update', kwargs={'pk': self.book.pk}), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Harry Potter")

    def test_update_book_unauthenticated(self):
        """Test that unauthenticated users cannot update a book"""
        data = {"title": "Unauthorized Update", "publication_year": 2025, "author": self.author.pk}
        response = self.client.put(reverse('book-update', kwargs={'pk': self.book.pk}), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class BookDeleteViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(title="Harry Potter", publication_year=1997, author=self.author)

    def test_delete_book_authenticated(self):
        """Test deleting a book as an authenticated user"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(reverse('book-delete', kwargs={'pk': self.book.pk}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_delete_book_unauthenticated(self):
        """Test that unauthenticated users cannot delete a book"""
        response = self.client.delete(reverse('book-delete', kwargs={'pk': self.book.pk}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
