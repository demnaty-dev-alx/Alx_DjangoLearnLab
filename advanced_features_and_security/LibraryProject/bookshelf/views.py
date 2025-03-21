from django.contrib.auth.decorators import permission_required
from django.shortcuts import HttpResponse, redirect, render
from .forms import ExampleForm

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    View to list all books.

    This view requires the user to have the 'can_view' permission in the 'bookshelf' app.
    If the user does not have this permission, a 403 Forbidden response will be returned.

    Arguments:
    - request: The HTTP request object.

    Returns:
    - HttpResponse: A response containing the list of books (in this case, a placeholder message).
    """
    return HttpResponse(content="List of Books")

@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    """
    View to create a new book.

    This view requires the user to have the 'can_create' permission in the 'bookshelf' app.
    If the user does not have this permission, a 403 Forbidden response will be returned.

    Arguments:
    - request: The HTTP request object.

    Returns:
    - HttpResponse: A response indicating that the book creation process has been triggered (placeholder message).
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new book to the database
            return redirect('book_list')  # Redirect to a page that lists books (you can modify this as needed)
    else:
        form = ExampleForm()

    return render(request, 'bookshelf/form_example.html', {'form': form})

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    """
    View to edit an existing book.

    This view requires the user to have the 'can_edit' permission in the 'bookshelf' app.
    If the user does not have this permission, a 403 Forbidden response will be returned.

    Arguments:
    - request: The HTTP request object.
    - book_id (int): The ID of the book to edit.

    Returns:
    - HttpResponse: A response indicating that the edit process for the specified book is triggered (placeholder message).
    """
    return HttpResponse(content=f"Edit Book {book_id}")

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    """
    View to delete a book.

    This view requires the user to have the 'can_delete' permission in the 'bookshelf' app.
    If the user does not have this permission, a 403 Forbidden response will be returned.

    Arguments:
    - request: The HTTP request object.
    - book_id (int): The ID of the book to delete.

    Returns:
    - HttpResponse: A response indicating that the delete process for the specified book is triggered (placeholder message).
    """
    return HttpResponse(content=f"Delete Book {book_id}")
