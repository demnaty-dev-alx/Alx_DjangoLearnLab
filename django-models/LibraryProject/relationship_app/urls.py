from django.urls import path
from .views import list_books, LibraryDetailView
from . import views
from .admin_view import admin_view
from .lebrarian_view import librarian_view
from .member_view import member_view
from django.contrib.auth.views import LogoutView, LoginView

app_name = 'relationship_app'

urlpatterns = [
    path('books/', list_books, name="books"),
    path('library/', LibraryDetailView.as_view(), name="library"),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html', next_page='relationship_app:books',redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('admin/', admin_view, name='admin'),
    path('librarian/', librarian_view, name='librarian'),
    path('member/', member_view, name='member'),
]