from django.urls import path
from .views import list_books, LibraryDetailView
from . import views
from django.contrib.auth.views import LogoutView, LoginView

app_name = 'relationship_app'

urlpatterns = [
    path('books/', list_books, name="books"),
    path('library/', LibraryDetailView.as_view(), name="library"),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html', next_page='relationship_app:books',redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('admin/', views.admin_view, name='admin'),
    path('librarian/', views.librarian_view, name='librarian'),
    path('member/', views.member_view, name='member'),
    path('add/', views.add_book, name='add_book'),
    path('edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
]