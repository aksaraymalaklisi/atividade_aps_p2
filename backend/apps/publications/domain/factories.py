import uuid
from apps.publications.domain.entities import PetEntity, PublicationEntity


class PublicationFactory:
    """
    Factory Pattern
    Ensures that a Publication is always created with a Pet, maintaining the 1:1 integrity.
    """

    @staticmethod
    def create_publication_with_pet(
        publisher_id: uuid.UUID,
        name: str,
        species: str,
        breed: str,
        size: str,
        gender: str,
        approximate_age: int,
        description: str,
        vaccinated: bool,
        neutered: bool,
        organization_id: uuid.UUID | None = None,
    ) -> tuple[PublicationEntity, PetEntity]:

        publication = PublicationEntity(
            publisher_id=publisher_id,
            organization_id=organization_id,
        )

        pet = PetEntity(
            publication_id=publication.id,  # Will be set fully after DB save, but we link what we can
            name=name,
            species=species,
            breed=breed,
            size=size,
            gender=gender,
            approximate_age=approximate_age,
            description=description,
            vaccinated=vaccinated,
            neutered=neutered,
        )

        publication.pet = pet

        return publication, pet
