from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Columns shown in admin list view
    list_filter = ('author', 'publication_year')  # Filters in the sidebar
    search_fields = ('title', 'author')  # Search functionality for title and author