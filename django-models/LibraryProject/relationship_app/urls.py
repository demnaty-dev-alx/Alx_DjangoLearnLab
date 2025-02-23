from django.urls import path
from .views import list_books, LibraryDetailView, user_login, user_logout, user_register

urlpatterns = [
    # URL pattern for login
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
