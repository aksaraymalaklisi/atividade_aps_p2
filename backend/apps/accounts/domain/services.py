from abc import ABC, abstractmethod


class PasswordHashServiceInterface(ABC):
    """
    Domain service interface for password hashing and verification.
    This abstracts away the specific algorithm (e.g., bcrypt, Argon2) or framework (e.g., Django) used.
    """

    @abstractmethod
    def hash(self, raw_password: str) -> str:
        """Hash a plain text password."""
        pass

    @abstractmethod
    def verify(self, raw_password: str, hashed_password: str) -> bool:
        """Verify a plain text password against a hashed password."""
        pass
