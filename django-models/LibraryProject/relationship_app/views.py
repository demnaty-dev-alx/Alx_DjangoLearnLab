from django.shortcuts import render, redirect, HttpResponse
from .models import Book, UserProfile
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test

def list_books(request):
      """Retrieves all books and renders a template displaying the list."""
      books = Book.objects.all()
      context = {'books': books}
      return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

def register(request):
    if request.user.is_authenticated:
        return redirect("relationship_app:books")
    elif request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("relationship_app:login")
    else:
        form = UserCreationForm()

    return render(request, "relationship_app/register.html", {"form": form})

def is_admin(user):
    if user.is_authenticated:
        return user.profile.role == UserProfile.Roles.ADMIN
    return False

@user_passes_test(is_admin)
def admin_view(request):
    return HttpResponse(content=f"Welcome {request.user.username} to the admin page")

def is_librarian(user):
    if user.is_authenticated:
        return user.profile.role == UserProfile.Roles.LIBRARIAN
    return False

@user_passes_test(is_librarian, login_url='relationship_app:login')
def librarian_view(request):
    return HttpResponse(content=f"Welcome {request.user.username} to the librarian page")

def is_member(user):
    if user.is_authenticated:
        return user.profile.role == UserProfile.Roles.MEMBER
    return False

@user_passes_test(is_member, login_url='relationship_app:login')
def member_view(request):
    return HttpResponse(content=f"Welcome {request.user.username} to the memeber page")
