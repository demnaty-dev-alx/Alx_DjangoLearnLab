from .models import Author, Book, Library, Librarian

# Query all books by a specific author
author = Author.objects.get(name="Mohammed")
books_1 = author.books.all()
books_2 = Book.objects.filter(author=author)
# does books_1 has the same items as books_2 ??

# List all books in a library
books_3 = Library.objects.get(name="Space").books.all()

# Retrieve the librarian for a library
library = Library.objects.get(name="Math")
librarian = Librarian.objects.get(library=library)
