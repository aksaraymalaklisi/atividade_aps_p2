from abc import abstractmethod

from apps.accounts.domain.entities import UserEntity
from core.base_repository import Repository


class UserRepositoryInterface(Repository[UserEntity]):
    """
    Interface for User repository.
    Defines the contract that any persistent storage (e.g., Django ORM) must fulfill.
    """

    @abstractmethod
    def find_by_email(self, email: str) -> UserEntity | None:
        """Find a user by their email address."""
        pass

    @abstractmethod
    def find_by_username(self, username: str) -> UserEntity | None:
        """Find a user by their username."""
        pass

    @abstractmethod
    def exists_by_email_or_username(self, email: str, username: str) -> bool:
        """Check if a user already exists with the given email or username."""
        pass
