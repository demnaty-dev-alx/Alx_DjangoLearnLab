from django.db import models

# Model to represent an Author
class Author(models.Model):
    # The name of the author (e.g., "J.K. Rowling")
    name = models.CharField(max_length=255)  # CharField is used to store a string of the author's name

    def __str__(self):
        # String representation of the Author object for easy readability in admin or shell
        return self.name


# Model to represent a Book
class Book(models.Model):
    # The title of the book (e.g., "Harry Potter and the Philosopher's Stone")
    title = models.CharField(max_length=255)  # CharField to store the book title

    # The year the book was published (e.g., 1997)
    publication_year = models.IntegerField()  # IntegerField to store the publication year

    # Foreign key to the Author model, establishing a one-to-many relationship
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    # The 'on_delete=models.CASCADE' means if an Author is deleted, all their Books will be deleted
    # The 'related_name="books"' allows us to access all books by an author using author.books

    def __str__(self):
        # String representation of the Book object for easy readability in admin or shell
        return self.title
