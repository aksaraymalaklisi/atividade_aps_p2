from typing import Any

from apps.publications.domain.entities import PublicationEntity
from apps.publications.domain.repositories import PublicationRepositoryInterface
from core.base_use_case import BaseUseCase


class ListPublicationsUseCase(BaseUseCase[dict[str, Any], tuple[list[PublicationEntity], int]]):
    """
    Use Case for listing publications with filters and pagination.
    Returns a tuple of (publications, total_count).
    """

    def __init__(self, repository: PublicationRepositoryInterface) -> None:
        self.repository = repository

    def execute(self, request: dict[str, Any]) -> tuple[list[PublicationEntity], int]:
        offset = request.get("offset", 0)
        limit = request.get("limit", 20)
        filters = request.get("filters", {})

        publications = self.repository.find_all(offset=offset, limit=limit, filters=filters)
        total_count = self.repository.count(filters=filters)

        return publications, total_count
