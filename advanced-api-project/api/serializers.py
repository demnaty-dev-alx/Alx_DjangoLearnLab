from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

# Serializer to represent the Book model
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']  # Explicitly defining the fields to serialize

    # Custom validation for the publication_year field
    def validate_publication_year(self, value):
        """
        This method validates that the publication year of the book is not in the future.
        If the publication year is greater than the current year, a validation error is raised.
        """
        if value > datetime.now().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


# Serializer to represent the Author model
class AuthorSerializer(serializers.ModelSerializer):
    # Nesting the BookSerializer to include all the books written by the author
    books = BookSerializer(many=True, read_only=True)  # 'many=True' because an author can have multiple books

    class Meta:
        model = Author
        fields = ['name', 'books']  # Serialize the author's name and their related books
