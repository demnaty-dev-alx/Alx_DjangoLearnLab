from django.urls import path
from .views import list_books, LibraryDetailView
from . import views
from django.contrib.auth.views import LogoutView, LoginView

app_name = 'relationship_app'

urlpatterns = [
    path('books/', list_books, name="books"),
    path('library/', LibraryDetailView.as_view(), name="library"),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register')
]