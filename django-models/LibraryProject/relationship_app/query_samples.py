from .models import Author, Book, Library, Librarian

# Query all books by a specific author
author_name = "Mohammed"
author = Author.objects.get(name=author_name)
books_1 = author.books.all()
books_2 = Book.objects.filter(author=author)
# does books_1 has the same items as books_2 ??

# List all books in a library
library_name = "space"
books_3 = Library.objects.get(name=library_name).books.all()

# Retrieve the librarian for a library
library = Library.objects.get(name=library_name)
librarian = Librarian.objects.get(library=library)
