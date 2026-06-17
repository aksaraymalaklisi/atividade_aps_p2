import uuid
from django.conf import settings
from django.db import models

from apps.organizations.models import Organization
from apps.publications.domain.value_objects import PetGender, PetSize, PublicationStatus


class Publication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="publications")
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, related_name="publications")
    status = models.CharField(
        max_length=50,
        choices=[(s.value, s.name) for s in PublicationStatus],
        default=PublicationStatus.ACTIVE.value,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Publication {self.id} ({self.status})"


class Pet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    publication = models.OneToOneField(Publication, on_delete=models.CASCADE, related_name="pet")
    name = models.CharField(max_length=255)
    species = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    size = models.CharField(
        max_length=50,
        choices=[(s.value, s.name) for s in PetSize],
        default=PetSize.MEDIUM.value,
    )
    gender = models.CharField(
        max_length=50,
        choices=[(g.value, g.name) for g in PetGender],
        default=PetGender.UNKNOWN.value,
    )
    approximate_age = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    vaccinated = models.BooleanField(default=False)
    neutered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.species})"


class PetImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="images")
    image = models.CharField(max_length=512)
    is_primary = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Image for {self.pet.name} (Primary: {self.is_primary})"
