from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    # Set the email field as the username field
    USERNAME_FIELD = "email"
    # 'email' and 'password' are required by default. We no longer require 'username'.
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Book(models.Model):
    """
    Represents a book in the library.
    Includes custom permissions for viewing, creating, editing, and deleting books.
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publication_date = models.DateField()

    class Meta:
        # Documentation: Custom permissions are defined here.
        # These can be assigned to groups in the Django admin panel.
        # 'Editors' group should get create, edit, and view permissions.
        # 'Viewers' group should only get the view permission.
        permissions = [
            ("can_view_book", "Can view book"),
            ("can_create_book", "Can create book"),
            ("can_edit_book", "Can edit book"),
            ("can_delete_book", "Can delete book"),
        ]

    def __str__(self):
        return self.title
