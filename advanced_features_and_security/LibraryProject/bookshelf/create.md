# Create a Book instance with the title "1984", author "George Orwell", and publication year 1949.
from bookshelf.models import Book

book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)  # Expected Output: 1984 by George Orwell (1949)
