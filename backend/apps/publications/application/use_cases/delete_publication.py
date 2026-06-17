import uuid

from apps.publications.domain.repositories import PublicationRepositoryInterface


class DeletePublicationUseCase:
    """
    Deletes a publication.
    """

    def __init__(self, repository: PublicationRepositoryInterface):
        self.repository = repository

    def execute(self, publication_id: uuid.UUID) -> None:
        publication = self.repository.get_by_id(publication_id)
        if not publication:
            raise ValueError("Publication not found")

        self.repository.delete(publication_id)
