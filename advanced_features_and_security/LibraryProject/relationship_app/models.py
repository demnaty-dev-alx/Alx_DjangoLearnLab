from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

User = get_user_model()

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

    class Meta:
        permissions = [
            ("can_add_book", "Can add a new book"),
            ("can_change_book", "Can change the details of a book"),
            ("can_delete_book", "Can delete a book"),
        ]

    def __str__(self):
        return f"{self.title} by {self.author.name}"


class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name="libraries")


class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.SET_NULL, null=True, blank=True)

class UserProfile(models.Model):

    class Roles(models.TextChoices):
        ADMIN = 'Admin', 'Admin'
        LIBRARIANS = 'Librarians', 'Librarians'
        MEMBER = 'Member', 'Member'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.MEMBER
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)