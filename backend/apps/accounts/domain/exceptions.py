from core.exceptions import ApplicationError


class UserAlreadyExistsError(ApplicationError):
    """Raised when trying to register a user with an email or username that is already taken."""

    def __init__(self, message: str = "User with this email or username already exists.") -> None:
        super().__init__(message=message, code="USER_ALREADY_EXISTS")


class InvalidCredentialsError(ApplicationError):
    """Raised when authentication fails due to wrong email or password."""

    def __init__(self, message: str = "Invalid email or password.") -> None:
        super().__init__(message=message, code="INVALID_CREDENTIALS")
