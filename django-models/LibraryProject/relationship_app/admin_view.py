from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

def is_admin(user):
    return user.userprofile.role == 'Admin'

class Admin(LoginRequiredMixin, View):
    @user_passes_test(is_admin)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'admin_view.html')