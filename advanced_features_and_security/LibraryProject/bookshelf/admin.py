from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Book

User = get_user_model()

class BookAdmin(admin.ModelAdmin):
    list_display = ["title","author","publication_year"]
    list_filter = ["author","publication_year"]
    search_fields = ["title", "author"]

admin.site.register(Book, BookAdmin)

class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_of_birth')

    fieldsets = (
        ('Login Credentials', {'fields': ('username', 'password')}),
        ('Personal Information', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)
