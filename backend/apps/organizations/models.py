import uuid

from django.conf import settings
from django.db import models

from apps.organizations.domain.value_objects import MembershipRole, OrganizationStatus


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    cnpj = models.CharField(max_length=20, unique=True, default="")
    email = models.EmailField(unique=True, default="")
    phone = models.CharField(max_length=20, blank=True, default="")
    address = models.TextField(blank=True, default="")
    description = models.TextField(blank=True)
    document_url = models.CharField(max_length=512, blank=True, null=True)
    status = models.CharField(
        max_length=50,
        choices=[(s.value, s.name) for s in OrganizationStatus],
        default=OrganizationStatus.PENDING.value,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.status})"


class Membership(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="members")
    role = models.CharField(
        max_length=50,
        choices=[(r.value, r.name) for r in MembershipRole],
        default=MembershipRole.MEMBER.value,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "organization")

    def __str__(self) -> str:
        return f"{self.user.email} - {self.organization.name} ({self.role})"
