import uuid
from typing import Any

from django.db import transaction

from apps.publications.domain.entities import PetEntity, PetImageEntity, PublicationEntity
from apps.publications.domain.repositories import PublicationRepositoryInterface
from apps.publications.models import Pet, PetImage, Publication


class DjangoPublicationRepository(PublicationRepositoryInterface):
    """
    Django ORM implementation of the PublicationRepositoryInterface.
    """

    def _to_entity(self, model: Publication) -> PublicationEntity:
        pet_model = getattr(model, "pet", None)
        pet_entity = None

        if pet_model:
            images = [
                PetImageEntity(
                    id=img.id,
                    pet_id=img.pet_id,
                    image=img.image,
                    is_primary=img.is_primary,
                    order=img.order,
                ) for img in pet_model.images.all()
            ]

            pet_entity = PetEntity(
                id=pet_model.id,
                publication_id=pet_model.publication_id,
                name=pet_model.name,
                species=pet_model.species,
                breed=pet_model.breed,
                size=pet_model.size,
                gender=pet_model.gender,
                approximate_age=pet_model.approximate_age,
                description=pet_model.description,
                vaccinated=pet_model.vaccinated,
                neutered=pet_model.neutered,
                images=images,
            )

        return PublicationEntity(
            id=model.id,
            publisher_id=model.publisher_id,
            organization_id=model.organization_id,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
            pet=pet_entity,
        )

    @transaction.atomic
    def save(self, publication: PublicationEntity) -> PublicationEntity:
        # Create or update Publication
        pub_model, _ = Publication.objects.update_or_create(
            id=publication.id,
            defaults={
                "publisher_id": publication.publisher_id,
                "organization_id": publication.organization_id,
                "status": publication.status,
            }
        )

        if publication.pet:
            # Create or update Pet
            pet_model, _ = Pet.objects.update_or_create(
                id=publication.pet.id,
                defaults={
                    "publication_id": pub_model.id,
                    "name": publication.pet.name,
                    "species": publication.pet.species,
                    "breed": publication.pet.breed,
                    "size": publication.pet.size,
                    "gender": publication.pet.gender,
                    "approximate_age": publication.pet.approximate_age,
                    "description": publication.pet.description,
                    "vaccinated": publication.pet.vaccinated,
                    "neutered": publication.pet.neutered,
                }
            )

            # Handle images (for simplicity, delete old and recreate)
            PetImage.objects.filter(pet_id=pet_model.id).delete()
            images_to_create = []
            for img in publication.pet.images:
                images_to_create.append(PetImage(
                    id=img.id,
                    pet_id=pet_model.id,
                    image=img.image,
                    is_primary=img.is_primary,
                    order=img.order,
                ))
            PetImage.objects.bulk_create(images_to_create)

        # Refresh from DB to get auto-populated fields like created_at
        pub_model.refresh_from_db()
        return self._to_entity(pub_model)

    def get_by_id(self, publication_id: uuid.UUID) -> PublicationEntity | None:
        try:
            model = Publication.objects.select_related("pet").prefetch_related("pet__images").get(id=publication_id)
            return self._to_entity(model)
        except Publication.DoesNotExist:
            return None

    def _apply_filters(self, qs, filters: dict | None) -> Any:
        if not filters:
            return qs

        if "status" in filters:
            qs = qs.filter(status=filters["status"])
        if "species" in filters:
            qs = qs.filter(pet__species__icontains=filters["species"])
        if "size" in filters:
            qs = qs.filter(pet__size=filters["size"])
        if "gender" in filters:
            qs = qs.filter(pet__gender=filters["gender"])
        if "organization_id" in filters:
            qs = qs.filter(organization_id=filters["organization_id"])

        return qs

    def find_all(self, offset: int = 0, limit: int = 20, filters: dict | None = None) -> list[PublicationEntity]:
        qs = Publication.objects.select_related("pet").prefetch_related("pet__images").order_by("-created_at")
        qs = self._apply_filters(qs, filters)
        models = qs[offset : offset + limit]
        return [self._to_entity(model) for model in models]

    def count(self, filters: dict | None = None) -> int:
        qs = Publication.objects.all()
        qs = self._apply_filters(qs, filters)
        return qs.count()

    def delete(self, publication_id: uuid.UUID) -> bool:
        deleted, _ = Publication.objects.filter(id=publication_id).delete()
        return deleted > 0
