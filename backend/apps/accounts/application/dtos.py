from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterUserInput:
    """Input DTO for the RegisterUserUseCase."""

    email: str
    username: str
    password: str
    first_name: str = ""
    last_name: str = ""
    phone: str = ""
    show_phone: bool = False


@dataclass(frozen=True)
class RegisterUserOutput:
    """Output DTO for the RegisterUserUseCase."""

    id: str
    email: str
    username: str


@dataclass(frozen=True)
class AuthenticateUserInput:
    """Input DTO for the AuthenticateUserUseCase. Accepts email or username."""

    email: str | None = None
    username: str | None = None
    password: str = ""

    def __post_init__(self):
        if not self.email and not self.username:
            raise ValueError("Either email or username must be provided.")


@dataclass(frozen=True)
class AuthenticateUserOutput:
    """Output DTO for the AuthenticateUserUseCase. Returns user basic info."""

    id: str
    email: str
    username: str
    is_operator: bool
