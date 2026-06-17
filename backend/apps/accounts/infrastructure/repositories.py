import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from apps.accounts.domain.entities import UserEntity
from apps.accounts.domain.repositories import UserRepositoryInterface
from apps.accounts.infrastructure.models import User as DjangoUserModel


class DjangoUserRepository(UserRepositoryInterface):
    """
    Implementation of UserRepositoryInterface using Django ORM.
    Responsible for mapping the Domain Entity (UserEntity) to the Django Model (User).
    """

    def _to_entity(self, model: DjangoUserModel) -> UserEntity:
        return UserEntity(
            id=model.id,
            email=model.email,
            username=model.username,
            first_name=model.first_name,
            last_name=model.last_name,
            phone=model.phone,
            show_phone=model.show_phone,
            is_operator=model.is_operator,
            is_active=model.is_active,
            password_hash=model.password,
        )

    def _update_model(self, model: DjangoUserModel, entity: UserEntity) -> None:
        model.email = entity.email
        model.username = entity.username
        model.first_name = entity.first_name
        model.last_name = entity.last_name
        model.phone = entity.phone
        model.show_phone = entity.show_phone
        model.is_operator = entity.is_operator
        model.is_active = entity.is_active
        model.password = entity.password_hash

    def save(self, entity: UserEntity) -> UserEntity:
        if not entity.id:
            entity.id = uuid.uuid4()

        model, _ = DjangoUserModel.objects.get_or_create(id=entity.id)
        self._update_model(model, entity)
        model.save()
        return entity

    def get_by_id(self, entity_id: str) -> UserEntity | None:
        # Using string for backward compatibility with some abstract methods,
        # but internally converting to UUID.
        return self.find_by_id(uuid.UUID(entity_id))

    def find_by_id(self, entity_id: uuid.UUID) -> UserEntity | None:
        try:
            model = DjangoUserModel.objects.get(id=entity_id)
            return self._to_entity(model)
        except ObjectDoesNotExist:
            return None

    def find_all(self, offset: int = 0, limit: int = 20) -> list[UserEntity]:
        models = DjangoUserModel.objects.all()[offset : offset + limit]
        return [self._to_entity(m) for m in models]

    def count(self) -> int:
        return DjangoUserModel.objects.count()

    def delete(self, entity_id: uuid.UUID) -> bool:
        deleted, _ = DjangoUserModel.objects.filter(id=entity_id).delete()
        return deleted > 0

    def find_by_email(self, email: str) -> UserEntity | None:
        try:
            model = DjangoUserModel.objects.get(email=email)
            return self._to_entity(model)
        except ObjectDoesNotExist:
            return None

    def find_by_username(self, username: str) -> UserEntity | None:
        try:
            model = DjangoUserModel.objects.get(username=username)
            return self._to_entity(model)
        except ObjectDoesNotExist:
            return None

    def exists_by_email_or_username(self, email: str, username: str) -> bool:
        return DjangoUserModel.objects.filter(Q(email=email) | Q(username=username)).exists()
