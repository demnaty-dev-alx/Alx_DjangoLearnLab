from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile
from django.shortcuts import HttpResponse


def is_librarian(user):
    if user.is_authenticated:
        return user.profile.role == UserProfile.Roles.LIBRARIAN
    return False

@user_passes_test(is_librarian, login_url='relationship_app:login')
def librarian_view(request):
    return HttpResponse(content=f"Welcome {request.user.username} to the librarian page")
