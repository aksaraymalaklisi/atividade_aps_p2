"""
Application-wide exception hierarchy.

All custom exceptions inherit from ApplicationError, allowing
consistent error handling across presentation and application layers.
"""


class ApplicationError(Exception):
    """Base exception for all application-level errors."""

    def __init__(self, message: str, code: str = "APPLICATION_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class NotFoundError(ApplicationError):
    """Raised when a requested entity does not exist."""

    def __init__(self, entity_name: str, entity_id: str):
        super().__init__(
            message=f"{entity_name} with id '{entity_id}' was not found.",
            code="NOT_FOUND",
        )


class ValidationError(ApplicationError):
    """Raised when input data fails domain validation rules."""

    def __init__(self, message: str, field: str | None = None):
        self.field = field
        super().__init__(message=message, code="VALIDATION_ERROR")


class AuthorizationError(ApplicationError):
    """Raised when a user lacks permission to perform an action."""

    def __init__(self, message: str = "You do not have permission to perform this action."):
        super().__init__(message=message, code="AUTHORIZATION_ERROR")


class ConflictError(ApplicationError):
    """Raised when an action conflicts with existing state (e.g., duplicate email)."""

    def __init__(self, message: str):
        super().__init__(message=message, code="CONFLICT")
