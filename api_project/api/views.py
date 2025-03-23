from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()  # Fetch all the books from the database
    serializer_class = BookSerializer  # Use the BookSerializer to serialize the data


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()  # Retrieve all Book objects from the database
    serializer_class = BookSerializer  # Use the BookSerializer to serialize the data
