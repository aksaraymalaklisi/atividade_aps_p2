"""
User repository interface (port).

Defines the contract that any user data access implementation must fulfill.
The domain and application layers depend on this interface,
not on concrete implementations (Dependency Inversion Principle).
"""

import uuid
from abc import abstractmethod

from core.base_repository import Repository
from apps.accounts.domain.entities import UserEntity


class UserRepositoryInterface(Repository[UserEntity]):
    """Repository contract for User entity persistence."""

    @abstractmethod
    def find_by_email(self, email: str) -> UserEntity | None:
        """Find a user by their email address."""

    @abstractmethod
    def find_by_username(self, username: str) -> UserEntity | None:
        """Find a user by their username."""

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """Check if a user with the given email already exists."""

    @abstractmethod
    def exists_by_username(self, username: str) -> bool:
        """Check if a user with the given username already exists."""
