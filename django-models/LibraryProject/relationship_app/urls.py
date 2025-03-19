from django.urls import path
from .views import list_books, LibraryDetailView, SignUpView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('books/', list_books, name="books"),
    path('library/', LibraryDetailView.as_view(), name="library"),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', SignUpView.as_view(), name='register')
]