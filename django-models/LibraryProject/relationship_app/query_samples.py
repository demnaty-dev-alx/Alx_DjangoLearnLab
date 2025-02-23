from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
    try:
        # Get the Author by name
        author = Author.objects.get(name=author_name)
        # Query all books by this author
        books = Book.objects.filter(author=author)
        print(f"Books by {author_name}:")
        for book in books:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print(f"Author with the name '{author_name}' does not exist.")

def list_books_in_library(library_name):
    try:
        # Get the Library by name
        library = Library.objects.get(name=library_name)
        # Query all books in this library
        books = library.books.all()
        print(f"Books in {library_name} Library:")
        for book in books:
            print(f"- {book.title}")
    except Library.DoesNotExist:
        print(f"Library with the name '{library_name}' does not exist.")

def retrieve_librarian_for_library(library_name):
    try:
        # Get the Library by name
        library = Library.objects.get(name=library_name)
        # Retrieve the librarian for this library
        librarian = Librarian.objects.get(library=library)
        print(f"The librarian for {library_name} is {librarian.name}.")
    except Library.DoesNotExist:
        print(f"Library with the name '{library_name}' does not exist.")
    except Librarian.DoesNotExist:
        print(f"No librarian found for the library '{library_name}'.")

# Query all books by a specific author
query_books_by_author("J.K. Rowling")

# List all books in a specific library
list_books_in_library("Central Library")

# Retrieve the librarian for a specific library
retrieve_librarian_for_library("Central Library")