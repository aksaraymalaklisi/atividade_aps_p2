from apps.publications.application.dtos import UpdatePublicationStatusInputDTO
from apps.publications.domain.repositories import PublicationRepositoryInterface
from apps.publications.domain.value_objects import PublicationStatus


class ChangePublicationStatusUseCase:
    """
    Changes the status of a publication (e.g., ADOPTED).
    """

    def __init__(self, repository: PublicationRepositoryInterface):
        self.repository = repository

    def execute(self, dto: UpdatePublicationStatusInputDTO) -> None:
        publication = self.repository.get_by_id(dto.publication_id)
        if not publication:
            raise ValueError("Publication not found")

        try:
            status_enum = PublicationStatus[dto.status]
        except KeyError as err:
            raise ValueError(f"Invalid status: {dto.status}") from err

        publication.status = status_enum.value
        self.repository.save(publication)
