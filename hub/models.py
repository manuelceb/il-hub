from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# superuser-> a@b.com user:a pass:a
# client id: M3NwNfUD7ZolzA5mb81InHAfzbuZjZrsluFtgjBj
# Client Secret: JlulM6yLZFBPiETqPvCRW0qHNPCoZrKs0qcPhmACVcRVUa9mvkHKqAH765vqTxkihB6UmjcOZYftuf3F0zYkkYYqKwlzYWhph7ETy7uIYi2CQ319uxg4DOc7G4X5TA1t

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
    - keep username for public profiles
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