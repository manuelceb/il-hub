from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.db import transaction


class Command(BaseCommand):
    help = "Project setup: migrations + seed database"

    def handle(self, *args, **options):

        self.stdout.write(self.style.MIGRATE_HEADING("Running migrate..."))
        call_command("migrate")

        # Users creation
        self.stdout.write(self.style.WARNING("Users creation..."))

        User = get_user_model()

        DEFAULT_USERS = [
            {
                "email": "admin@ilhub.com",
                "password": "admin123",
                "is_staff": True,
                "is_superuser": True,
            },
            {
                "email": "ilhub.user1@gmail.com",
                "password": "demo123",
                "is_staff": False,
                "is_superuser": False,
            },
            {
                "email": "ilhub.user2@gmail.com",
                "password": "demo123",
                "is_staff": False,
                "is_superuser": False,
            },
        ]

        with transaction.atomic():
            for user_data in DEFAULT_USERS:
                email = user_data["email"]
                password = user_data["password"]
                if User.objects.filter(email=email).exists():
                    continue
                if user_data["is_superuser"]:
                    User.objects.create_superuser(
                        email=email,
                        password=password,
                    )
                else:
                    User.objects.create_user(
                        email=email,
                        password=password,
                        is_staff=user_data["is_staff"],
                        is_superuser=user_data["is_superuser"],
                    )

        self.stdout.write(self.style.SUCCESS("Project ready!"))
