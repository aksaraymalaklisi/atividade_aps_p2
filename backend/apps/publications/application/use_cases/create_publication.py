from apps.publications.application.dtos import CreatePublicationInputDTO, CreatePublicationOutputDTO
from apps.publications.application.observers import publication_event_publisher
from apps.publications.application.strategies import ImageUploadStrategy
from apps.publications.domain.entities import PetImageEntity
from apps.publications.domain.factories import PublicationFactory
from apps.publications.domain.repositories import PublicationRepositoryInterface
from core.base_use_case import BaseUseCase


class CreatePublicationUseCase(BaseUseCase[CreatePublicationInputDTO, CreatePublicationOutputDTO]):
    """
    Use Case for creating a publication and its associated pet.
    """

    def __init__(
        self,
        repository: PublicationRepositoryInterface,
        image_strategy: ImageUploadStrategy,
    ) -> None:
        self.repository = repository
        self.image_strategy = image_strategy

    def execute(self, request: CreatePublicationInputDTO) -> CreatePublicationOutputDTO:
        # Create entities via Factory
        publication, pet = PublicationFactory.create_publication_with_pet(
            publisher_id=request.publisher_id,
            name=request.name,
            species=request.species,
            breed=request.breed,
            size=request.size,
            gender=request.gender,
            approximate_age=request.approximate_age,
            description=request.description,
            vaccinated=request.vaccinated,
            neutered=request.neutered,
            organization_id=request.organization_id,
        )

        # Upload images
        for idx, file_obj in enumerate(request.images):
            image_url = self.image_strategy.upload(file_obj.name, file_obj)
            is_primary = idx == 0
            pet_image = PetImageEntity(
                image=image_url,
                is_primary=is_primary,
                order=idx,
            )
            pet.images.append(pet_image)

        # Save to DB
        saved_publication = self.repository.save(publication)

        # Notify observers
        publication_event_publisher.notify_created(saved_publication)

        return CreatePublicationOutputDTO(
            publication_id=saved_publication.id,
            pet_id=saved_publication.pet.id,
            status=saved_publication.status,
        )
