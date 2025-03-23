from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()  # Fetch all the books from the database
    serializer_class = BookSerializer  # Use the BookSerializer to serialize the data


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Book.objects.all()  # Retrieve all Book objects from the database
    serializer_class = BookSerializer  # Use the BookSerializer to serialize the data

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
