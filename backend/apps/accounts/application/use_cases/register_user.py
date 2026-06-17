from apps.accounts.application.dtos import RegisterUserInput, RegisterUserOutput
from apps.accounts.domain.entities import UserEntity
from apps.accounts.domain.exceptions import UserAlreadyExistsError
from apps.accounts.domain.repositories import UserRepositoryInterface
from apps.accounts.domain.services import PasswordHashServiceInterface
from core.base_use_case import BaseUseCase


class RegisterUserUseCase(BaseUseCase[RegisterUserInput, RegisterUserOutput]):
    """
    Use Case for registering a new user in the platform.

    This use case enforces the business rule that a user's email and username
    must be unique across the platform.
    """

    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        hash_service: PasswordHashServiceInterface
    ) -> None:
        self.user_repository = user_repository
        self.hash_service = hash_service

    def execute(self, request: RegisterUserInput) -> RegisterUserOutput:
        # Check if user already exists
        if self.user_repository.exists_by_email_or_username(request.email, request.username):
            raise UserAlreadyExistsError()

        hashed_password = self.hash_service.hash(request.password)

        # Create domain entity
        new_user = UserEntity(
            email=request.email,
            username=request.username,
            first_name=request.first_name,
            last_name=request.last_name,
            phone=request.phone,
            show_phone=request.show_phone,
            is_active=True,
            is_operator=False,
            password_hash=hashed_password,
        )

        # Save via repository (which handles ID generation and persistence)
        saved_user = self.user_repository.save(new_user)

        # Return output DTO
        return RegisterUserOutput(
            id=str(saved_user.id),
            email=saved_user.email,
            username=saved_user.username,
        )
