# create.md

# Create a Book instance with the title "1984", author "George Orwell", and publication year 1949.
from bookshelf.models import Book

book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)  # Expected Output: <Book: 1984 by George Orwell (1949)>

# retrieve.md

# Retrieve and display all attributes of the book just created.
from bookshelf.models import Book

book = Book.objects.get(title="1984")
print(f"Title: {book.title}, Author: {book.author}, Year: {book.publication_year}")

# Expected Output:
# Title: 1984, Author: George Orwell, Year: 1949

# update.md

# Update the title of "1984" to "Nineteen Eighty-Four" and save the changes.
from bookshelf.models import Book

book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Retrieve and check the updated title
updated_book = Book.objects.get(id=book.id)
print(f"Updated Title: {updated_book.title}")

# Expected Output:
# Updated Title: Nineteen Eighty-Four

# delete.md

# Delete the book and confirm deletion
from bookshelf.models import Book

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Try retrieving all books again
books = Book.objects.all()
print(list(books))  # Expected Output: List of books without the deleted entry
