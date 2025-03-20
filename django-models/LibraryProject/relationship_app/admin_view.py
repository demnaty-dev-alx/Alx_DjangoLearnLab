from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile
from django.shortcuts import HttpResponse, render

def is_admin(user):
    if user.is_authenticated:
        return user.profile.role == 'Admin'
    return False

@user_passes_test(is_admin, login_url='relationship_app:login')
def admin_view(request):
    return render(request, 'admin_view.html')
