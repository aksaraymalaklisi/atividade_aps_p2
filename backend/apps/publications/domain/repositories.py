import uuid
from abc import ABC, abstractmethod

from apps.publications.domain.entities import PublicationEntity


class PublicationRepositoryInterface(ABC):
    """Repository interface for Publication entity."""

    @abstractmethod
    def save(self, publication: PublicationEntity) -> PublicationEntity:
        pass

    @abstractmethod
    def get_by_id(self, publication_id: uuid.UUID) -> PublicationEntity | None:
        pass

    @abstractmethod
    def find_all(self, offset: int = 0, limit: int = 20, filters: dict | None = None) -> list[PublicationEntity]:
        pass

    @abstractmethod
    def count(self, filters: dict | None = None) -> int:
        pass

    @abstractmethod
    def delete(self, publication_id: uuid.UUID) -> bool:
        pass
