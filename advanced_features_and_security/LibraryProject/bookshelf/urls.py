from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    path('add/', views.create_book, name="add"),
    path('edit/<book_id>/', views.edit_book, name="edit"),
    path('view/', views.book_list, name="view"),
    path('delete/<book_id>/', views.delete_book, name="delete"),
]