>>> from bookshelf.models import Book
>>> book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
>>> print(book)
1984 by George Orwell (1949)
>>> retrieved_book = Book.objects.get(title="1984")
>>> print(f"Title: {retrieved_book.title}, Author: {retrieved_book.author}, Year: {retrieved_book.publication_year}")
Title: 1984, Author: George Orwell, Year: 1949
>>> retrieved_book.title = "Nineteen Eighty-Four"
>>> retrieved_book.save()
>>> print(f"Updated Title: {retrieved_book.title}")
Updated Title: Nineteen Eighty-Four
>>> retrieved_book.delete()
(1, {'bookshelf.Book': 1})
>>> print(Book.objects.all())
<QuerySet []>