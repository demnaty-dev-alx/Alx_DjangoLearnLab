from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Library, Book, UserProfile
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

def list_books(request):
    books = Book.objects.all()  # Retrieve all books from the database
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'  # To access the library object in the template

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return redirect('login')  # Redirect to login page after registration
    else:
        form = UserCreationForm()

    return render(request, 'relationship_app/register.html', {'form': form})

# Function to check if the user is an Admin
def is_admin(user):
    return user.userprofile.role == 'Admin'

# Function to check if the user is a Librarian
def is_librarian(user):
    return user.userprofile.role == 'Librarian'

# Function to check if the user is a Member
def is_member(user):
    return user.userprofile.role == 'Member'

# Admin view (restricted to Admins)
@user_passes_test(is_admin)
def admin(request):
    return render(request, 'relationship_app/admin_view.html')

# Librarian view (restricted to Librarians)
@user_passes_test(is_librarian)
def librarian(request):
    return render(request, 'relationship_app/librarian_view.html')

# Member view (restricted to Members)
@user_passes_test(is_member)
def member(request):
    return render(request, 'relationship_app/member_view.html')

from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    return redirect('book_list')

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    return redirect('book_list')

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    return redirect('book_list')
