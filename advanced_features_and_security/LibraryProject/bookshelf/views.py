from django.contrib.auth.decorators import permission_required
from django.shortcuts import HttpResponse
from .models import Book

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    return HttpResponse(content="List of Books")

@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    return HttpResponse(content="Create Book")

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    return HttpResponse(content=f"Edit Book {book_id}")

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    return HttpResponse(content=f"Delete Book {book_id}")

