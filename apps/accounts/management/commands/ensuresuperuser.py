import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create or update a superuser from environment variables."

    def handle(self, *args, **options):
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip().lower()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")
        first_name = os.environ.get("DJANGO_SUPERUSER_FIRST_NAME", "").strip()
        last_name = os.environ.get("DJANGO_SUPERUSER_LAST_NAME", "").strip()
        affiliation = os.environ.get("DJANGO_SUPERUSER_AFFILIATION", "").strip()

        if not email or not password:
            raise CommandError(
                "DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD must be set."
            )

        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            email=email,
            defaults={
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
                "is_email_verified": True,
            },
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.is_email_verified = True

        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if affiliation:
            user.affiliation = affiliation

        user.set_password(password)
        user.save()

        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action} superuser {email}"))
