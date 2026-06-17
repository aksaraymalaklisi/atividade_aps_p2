import pytest

from apps.accounts.application.dtos import AuthenticateUserInput
from apps.accounts.application.use_cases.authenticate_user import AuthenticateUserUseCase
from apps.accounts.domain.entities import UserEntity
from apps.accounts.domain.exceptions import InvalidCredentialsError
from apps.accounts.domain.services import PasswordHashServiceInterface
from apps.accounts.tests.unit.in_memory_repository import InMemoryUserRepository


class DummyPasswordHashService(PasswordHashServiceInterface):
    def hash(self, raw_password: str) -> str:
        return f"hashed_{raw_password}"

    def verify(self, raw_password: str, hashed_password: str) -> bool:
        return f"hashed_{raw_password}" == hashed_password


@pytest.fixture
def user_repo() -> InMemoryUserRepository:
    return InMemoryUserRepository()


@pytest.fixture
def hash_service() -> DummyPasswordHashService:
    return DummyPasswordHashService()


@pytest.fixture
def auth_use_case(user_repo: InMemoryUserRepository, hash_service: DummyPasswordHashService) -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase(user_repository=user_repo, hash_service=hash_service)


@pytest.fixture
def seeded_user(user_repo: InMemoryUserRepository, hash_service: DummyPasswordHashService) -> UserEntity:
    user = UserEntity(
        email="login@example.com",
        username="loginuser",
        is_active=True,
    )
    # Password should be saved hashed in the entity (or another abstraction)
    # But for this test, let's attach the hash as an attribute. In a real system,
    # the entity would have a password_hash property.
    user.password_hash = hash_service.hash("CorrectPassword123!")
    return user_repo.save(user)


def test_authenticate_user_with_email_success(auth_use_case: AuthenticateUserUseCase, seeded_user: UserEntity):
    input_dto = AuthenticateUserInput(email=seeded_user.email, password="CorrectPassword123!")
    output = auth_use_case.execute(input_dto)

    assert output.id == str(seeded_user.id)
    assert output.email == seeded_user.email


def test_authenticate_user_with_username_success(auth_use_case: AuthenticateUserUseCase, seeded_user: UserEntity):
    input_dto = AuthenticateUserInput(username=seeded_user.username, password="CorrectPassword123!")
    output = auth_use_case.execute(input_dto)

    assert output.id == str(seeded_user.id)
    assert output.username == seeded_user.username


def test_authenticate_user_with_wrong_password_fails(auth_use_case: AuthenticateUserUseCase, seeded_user: UserEntity):
    input_dto = AuthenticateUserInput(email=seeded_user.email, password="WrongPassword!")
    with pytest.raises(InvalidCredentialsError):
        auth_use_case.execute(input_dto)


def test_authenticate_user_not_found_fails(auth_use_case: AuthenticateUserUseCase):
    input_dto = AuthenticateUserInput(email="nonexistent@example.com", password="CorrectPassword123!")
    with pytest.raises(InvalidCredentialsError):
        auth_use_case.execute(input_dto)


def test_authenticate_inactive_user_fails(
    user_repo: InMemoryUserRepository,
    hash_service: DummyPasswordHashService,
    auth_use_case: AuthenticateUserUseCase,
):
    user = UserEntity(email="inactive@example.com", username="inactive", is_active=False)
    user.password_hash = hash_service.hash("CorrectPassword123!")
    user_repo.save(user)

    input_dto = AuthenticateUserInput(email="inactive@example.com", password="CorrectPassword123!")
    with pytest.raises(InvalidCredentialsError):
        auth_use_case.execute(input_dto)
