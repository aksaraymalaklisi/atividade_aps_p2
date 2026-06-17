"""Accounts domain exceptions."""

from core.exceptions import NotFoundError, ConflictError


class UserNotFoundError(NotFoundError):
    def __init__(self, identifier: str):
        super().__init__(entity_name="User", entity_id=identifier)


class EmailAlreadyExistsError(ConflictError):
    def __init__(self, email: str):
        super().__init__(message=f"A user with email '{email}' already exists.")


class UsernameAlreadyExistsError(ConflictError):
    def __init__(self, username: str):
        super().__init__(message=f"A user with username '{username}' already exists.")
