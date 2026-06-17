"""
Base repository interfaces for the domain layer.

These abstract classes define the contracts that infrastructure
implementations must fulfill. Use cases depend on these abstractions,
not on concrete implementations (Dependency Inversion Principle).

Repositories are segregated into read/write interfaces following
the Interface Segregation Principle (ISP).
"""

import uuid
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from core.base_entity import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class ReadableRepository(ABC, Generic[T]):
    """Interface for read-only data access operations."""

    @abstractmethod
    def find_by_id(self, entity_id: uuid.UUID) -> T | None:
        """Retrieve an entity by its unique identifier."""

    @abstractmethod
    def find_all(self, offset: int = 0, limit: int = 20) -> list[T]:
        """Retrieve a paginated list of entities."""

    @abstractmethod
    def count(self) -> int:
        """Return the total number of entities."""


class WritableRepository(ABC, Generic[T]):
    """Interface for write data access operations."""

    @abstractmethod
    def save(self, entity: T) -> T:
        """Persist an entity (create or update)."""

    @abstractmethod
    def delete(self, entity_id: uuid.UUID) -> bool:
        """Remove an entity by its unique identifier. Returns True if deleted."""


class Repository(ReadableRepository[T], WritableRepository[T], ABC):
    """
    Combined read/write repository interface.

    Use this when a use case needs both read and write access.
    Prefer the segregated interfaces (ReadableRepository, WritableRepository)
    when only one type of access is needed.
    """
