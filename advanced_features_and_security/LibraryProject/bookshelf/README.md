# Permissions & Groups Setup for Bookstore App

## Step 1: Custom Permissions in the Book Model
We have defined custom permissions in the `Book` model to control actions such as viewing, creating, editing, and deleting book records.

### Defined Permissions:
| Permission Codename | Description |
|---------------------|-------------|
| `can_view`  | Can view book records |
| `can_create`  | Can create a book |
| `can_edit`  | Can edit a book |
| `can_delete`  | Can delete a book |

These permissions are defined in the `Meta` class inside the `Book` model:

```python
class Meta:
    permissions = [
        ("can_view", "Can view book"),
        ("can_create", "Can create book"),
        ("can_edit", "Can edit book"),
        ("can_delete", "Can delete book"),
    ]
```

---

## Step 2: User Groups & Permissions
We have created three user groups in Django and assigned them permissions.

| Group | Assigned Permissions |
|-------|----------------------|
| **Viewers** | `can_view` |
| **Editors** | `can_view`, `can_create`, `can_edit` |
| **Admins** | `can_view`, `can_create`, `can_edit`, `can_delete` |

To create these groups and assign permissions, run the following script inside Django shell:

```python
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookstore.models import Book

# Get the content type for the Book model
book_content_type = ContentType.objects.get_for_model(Book)

# Define permissions
can_view = Permission.objects.get(codename="can_view", content_type=book_content_type)
can_create = Permission.objects.get(codename="can_create", content_type=book_content_type)
can_edit = Permission.objects.get(codename="can_edit", content_type=book_content_type)
can_delete = Permission.objects.get(codename="can_delete", content_type=book_content_type)

# Create groups
viewers_group, _ = Group.objects.get_or_create(name="Viewers")
viewers_group.permissions.add(can_view)

editors_group, _ = Group.objects.get_or_create(name="Editors")
editors_group.permissions.add(can_view, can_create, can_edit)

admins_group, _ = Group.objects.get_or_create(name="Admins")
admins_group.permissions.add(can_view, can_create, can_edit, can_delete)

print("Groups and permissions set up successfully.")
```

Run this script using:

```sh
python manage.py shell
```

---

## Step 3: Enforcing Permissions in Views

### Function-Based Views (FBVs)
```python
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from bookstore.models import Book

@permission_required('bookstore.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return HttpResponse(books)

@permission_required('bookstore.can_create', raise_exception=True)
def create_book(request):
    if request.method == "POST":
        # Logic to create a book
        return redirect("book_list")
    return HttpResponse("Create Book Page")

@permission_required('bookstore.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        # Logic to edit the book
        return redirect("book_list")
    return HttpResponse(f"Edit Book {book.title}")

@permission_required('bookstore.can_delete', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect("book_list")
```

---

## Step 4: Testing
1. **Create test users** and assign them to different groups in Django Admin.
2. **Log in as each user** and check if permissions are applied correctly.
3. **Try to access restricted views** (create, edit, delete) with users who lack permissions.

---

## Step 5: Managing Groups & Users in Django Admin
To manage user groups, log in to Django Admin:

1. **Navigate to `/admin/`**
2. **Go to "Groups"**
3. **Assign permissions** to groups or users manually if needed.