import uuid

from apps.publications.application.dtos import UpdatePublicationInputDTO
from apps.publications.application.strategies import ImageUploadStrategy
from apps.publications.domain.entities import PetImageEntity
from apps.publications.domain.repositories import PublicationRepositoryInterface


class UpdatePublicationUseCase:
    """
    Updates an existing publication and its associated pet.
    """

    def __init__(self, repository: PublicationRepositoryInterface, image_strategy: ImageUploadStrategy):
        self.repository = repository
        self.image_strategy = image_strategy

    def execute(self, dto: UpdatePublicationInputDTO) -> None:
        publication = self.repository.get_by_id(dto.publication_id)
        if not publication:
            raise ValueError("Publication not found")

        if publication.pet:
            if dto.name is not None:
                publication.pet.name = dto.name
            if dto.species is not None:
                publication.pet.species = dto.species
            if dto.breed is not None:
                publication.pet.breed = dto.breed
            if dto.size is not None:
                publication.pet.size = dto.size
            if dto.gender is not None:
                publication.pet.gender = dto.gender
            if dto.approximate_age is not None:
                publication.pet.approximate_age = dto.approximate_age
            if dto.description is not None:
                publication.pet.description = dto.description
            if dto.vaccinated is not None:
                publication.pet.vaccinated = dto.vaccinated
            if dto.neutered is not None:
                publication.pet.neutered = dto.neutered

            if dto.images is not None and len(dto.images) > 0:
                # If new images are provided, we replace the old ones.
                new_images = []
                for idx, file_obj in enumerate(dto.images):
                    image_url = self.image_strategy.upload(file_obj.name, file_obj)
                    is_primary = idx == 0
                    new_images.append(
                        PetImageEntity(
                            id=uuid.uuid4(),
                            pet_id=publication.pet.id,
                            image=image_url,
                            is_primary=is_primary,
                            order=idx,
                        )
                    )
                publication.pet.images = new_images

        self.repository.save(publication)
