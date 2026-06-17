import uuid

from apps.accounts.domain.entities import UserEntity
from apps.accounts.domain.repositories import UserRepositoryInterface


class InMemoryUserRepository(UserRepositoryInterface):
    """In-memory implementation of the UserRepositoryInterface for unit testing."""

    def __init__(self) -> None:
        self.users: dict[str, UserEntity] = {}

    def save(self, entity: UserEntity) -> UserEntity:
        if not entity.id:
            entity.id = uuid.uuid4()
        self.users[str(entity.id)] = entity
        return entity

    def get_by_id(self, entity_id: str) -> UserEntity | None:
        return self.users.get(entity_id)

    def find_by_id(self, entity_id: uuid.UUID) -> UserEntity | None:
        return self.users.get(str(entity_id))

    def find_all(self, offset: int = 0, limit: int = 20) -> list[UserEntity]:
        return list(self.users.values())[offset : offset + limit]

    def count(self) -> int:
        return len(self.users)

    def delete(self, entity_id: uuid.UUID) -> bool:
        id_str = str(entity_id)
        if id_str in self.users:
            del self.users[id_str]
            return True
        return False

    def find_by_email(self, email: str) -> UserEntity | None:
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def find_by_username(self, username: str) -> UserEntity | None:
        for user in self.users.values():
            if user.username == username:
                return user
        return None

    def exists_by_email_or_username(self, email: str, username: str) -> bool:
        return self.find_by_email(email) is not None or self.find_by_username(username) is not None
