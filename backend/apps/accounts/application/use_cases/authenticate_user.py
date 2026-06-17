from apps.accounts.application.dtos import AuthenticateUserInput, AuthenticateUserOutput
from apps.accounts.domain.exceptions import InvalidCredentialsError
from apps.accounts.domain.repositories import UserRepositoryInterface
from apps.accounts.domain.services import PasswordHashServiceInterface
from core.base_use_case import BaseUseCase


class AuthenticateUserUseCase(BaseUseCase[AuthenticateUserInput, AuthenticateUserOutput]):
    """
    Use Case for authenticating a user via email or username and password.
    """

    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        hash_service: PasswordHashServiceInterface,
    ) -> None:
        self.user_repository = user_repository
        self.hash_service = hash_service

    def execute(self, request: AuthenticateUserInput) -> AuthenticateUserOutput:
        # Find user by email or username
        user = None
        if request.email:
            user = self.user_repository.find_by_email(request.email)
        elif request.username:
            user = self.user_repository.find_by_username(request.username)

        # Fail if not found or inactive
        if not user or not user.is_active:
            raise InvalidCredentialsError()

        # Verify password
        is_valid_password = self.hash_service.verify(
            raw_password=request.password,
            hashed_password=user.password_hash,
        )

        if not is_valid_password:
            raise InvalidCredentialsError()

        # Return output
        return AuthenticateUserOutput(
            id=str(user.id),
            email=user.email,
            username=user.username,
            is_operator=user.is_operator,
            is_staff=user.is_staff,
        )
