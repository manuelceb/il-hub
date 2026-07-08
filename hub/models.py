from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

import os
import uuid

# using UUID to avoid collisions with similar file names
def profile_photo_uuid(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f"profiles/{uuid.uuid4().hex}{ext}"

""" The following custom manager and custom user implementation 
    is based on: https://testdriven.io/blog/django-custom-user-model/
"""

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The email field must be set")

        email = self.normalize_email(email)

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)

        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    """
    Custom User:
    - login by email
    - Use email as the primary identifier for authentication
    """
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    bio = models.TextField(blank=True, default="")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return f"{self.get_full_name()}"
    
class LibraryInterestTopics(models.Model):
    topics = models.CharField(max_length=70, unique=True, blank=False)

    def __str__(self):
        return self.topics
    
class LibraryContext(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="library_context")
    nickname = models.CharField(max_length=200, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    interest_topics = models.ManyToManyField(LibraryInterestTopics)
    email_notifications = models.BooleanField(default=False)
    photo_path = models.ImageField(upload_to=profile_photo_uuid, blank=True, null=True)

class BlogTopics(models.Model):
    topics = models.CharField(max_length=70, unique=True, blank=False)

    def __str__(self):
        return self.topics
    
class BlogContext(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="blog_context")
    nickname = models.CharField(max_length=200, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    email_notifications = models.BooleanField(default=False)
    photo_path = models.ImageField(upload_to=profile_photo_uuid, blank=True, null=True)
    topics = models.ManyToManyField(BlogTopics)

