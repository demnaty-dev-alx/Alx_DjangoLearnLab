# Delete the book and confirm deletion
from bookshelf.models import Book

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Try retrieving all books again
books = Book.objects.all()
print(list(books))  # Expected Output: List of books without the deleted entry
