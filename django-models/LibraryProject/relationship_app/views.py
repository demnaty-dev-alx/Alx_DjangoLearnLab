from django.shortcuts import render, redirect
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
#from .admin_view import AdminView
from .lebrarian_view import librarian_view
from .member_view import member_view

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

from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile
from django.shortcuts import HttpResponse

def is_admin(user):
    if user.is_authenticated:
        return user.profile.role == UserProfile.Roles.ADMIN
    return False

@user_passes_test(is_admin, login_url='relationship_app:login')
def Admin(request):
    return HttpResponse(content=f"Welcome {request.user.username} to the admin page")
