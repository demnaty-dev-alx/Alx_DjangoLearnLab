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
