"""
Custom User model for PetAdopt.

This is the Django ORM model that lives in the infrastructure layer.
It maps the domain entity (UserEntity) to the database.
"""

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.

    Uses UUID as primary key and adds platform-specific fields:
    phone number, phone visibility preference, and operator role.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, default="")
    show_phone = models.BooleanField(
        default=False,
        help_text="If True, phone number is publicly visible on publications.",
    )
    is_operator = models.BooleanField(
        default=False,
        help_text="Operators can manage all platform aspects.",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "accounts_user"
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self) -> str:
        return self.email
