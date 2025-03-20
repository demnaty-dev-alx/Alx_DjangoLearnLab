from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile
from django.shortcuts import HttpResponse


def is_member(user):
    if user.is_authenticated:
        return user.profile.role == UserProfile.Roles.MEMBER
    return False

@user_passes_test(is_member, login_url='relationship_app:login')
def member_view(request):
    return HttpResponse(content=f"Welcome {request.user.username} to the memeber page")
