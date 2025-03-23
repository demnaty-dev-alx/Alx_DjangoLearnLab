from django.contrib import admin
from .models import Author, Book

# Register the Author model
admin.site.register(Author)

# Register the Book model
admin.site.register(Book)
