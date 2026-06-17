import pytest

from apps.accounts.application.dtos import RegisterUserInput
from apps.accounts.application.use_cases.register_user import RegisterUserUseCase
from apps.accounts.domain.exceptions import UserAlreadyExistsError
from apps.accounts.tests.unit.in_memory_repository import InMemoryUserRepository


@pytest.fixture
def user_repo() -> InMemoryUserRepository:
    return InMemoryUserRepository()


@pytest.fixture
def register_use_case(user_repo: InMemoryUserRepository) -> RegisterUserUseCase:
    return RegisterUserUseCase(user_repository=user_repo)


def test_register_user_creates_new_user_successfully(
    user_repo: InMemoryUserRepository, register_use_case: RegisterUserUseCase
):
    """Test that a user can be registered successfully when email and username are available."""
    input_dto = RegisterUserInput(
        email="test@example.com",
        username="testuser",
        password="SecurePassword123!",
        first_name="Test",
        last_name="User",
    )

    output = register_use_case.execute(input_dto)

    assert output.id is not None
    assert output.email == "test@example.com"
    assert output.username == "testuser"

    # Verify user was saved in repository
    saved_user = user_repo.find_by_email("test@example.com")
    assert saved_user is not None
    assert str(saved_user.id) == output.id
    assert saved_user.first_name == "Test"
    assert saved_user.last_name == "User"


def test_register_user_fails_if_email_or_username_exists(
    register_use_case: RegisterUserUseCase,
):
    """Test that registration fails if the user already exists."""
    input_dto = RegisterUserInput(
        email="test@example.com",
        username="testuser",
        password="SecurePassword123!",
    )

    # First registration should succeed
    register_use_case.execute(input_dto)

    # Second registration with same email should raise exception
    with pytest.raises(UserAlreadyExistsError):
        register_use_case.execute(input_dto)

    # Registration with different email but same username should fail
    input_dto_same_username = RegisterUserInput(
        email="another@example.com",
        username="testuser",
        password="SecurePassword123!",
    )
    with pytest.raises(UserAlreadyExistsError):
        register_use_case.execute(input_dto_same_username)
