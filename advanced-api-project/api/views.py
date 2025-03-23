from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters import rest_framework as rf
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    """
    API endpoint to list all books with filtering, searching, and ordering capabilities.
    Accessible to unauthenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [rf.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'author__name', 'publication_year']  # Allow filtering
    search_fields = ['title', 'author__name']  # Allow searching
    ordering_fields = ['title', 'publication_year']  # Allow ordering
    ordering = ['title']  # Default ordering
    permission_classes = [IsAuthenticatedOrReadOnly]  # Publicly accessible


class BookDetailView(generics.RetrieveAPIView):
    """
    API endpoint to retrieve a single book by its ID.
    Accessible to unauthenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Publicly accessible


class BookCreateView(generics.CreateAPIView):
    """
    API endpoint to create a new book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can create


class BookUpdateView(generics.UpdateAPIView):
    """
    API endpoint to update an existing book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can update


class BookDeleteView(generics.DestroyAPIView):
    """
    API endpoint to delete a book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can delete
