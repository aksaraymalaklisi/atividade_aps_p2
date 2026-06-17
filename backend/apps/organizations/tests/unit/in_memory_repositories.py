import uuid

from apps.organizations.domain.entities import MembershipEntity, OrganizationEntity
from apps.organizations.domain.repositories import (
    MembershipRepositoryInterface,
    OrganizationRepositoryInterface,
)
from apps.organizations.domain.value_objects import OrganizationStatus


class InMemoryOrganizationRepository(OrganizationRepositoryInterface):
    def __init__(self):
        self.organizations: dict[uuid.UUID, OrganizationEntity] = {}

    def save(self, entity: OrganizationEntity) -> OrganizationEntity:
        self.organizations[entity.id] = entity
        return entity

    def find_by_id(self, id: uuid.UUID) -> OrganizationEntity | None:
        return self.organizations.get(id)

    def delete(self, id: uuid.UUID) -> None:
        if id in self.organizations:
            del self.organizations[id]

    def find_all(self, offset: int = 0, limit: int = 20) -> list[OrganizationEntity]:
        return list(self.organizations.values())[offset : offset + limit]

    def count(self) -> int:
        return len(self.organizations)

    def find_by_name(self, name: str) -> OrganizationEntity | None:
        for org in self.organizations.values():
            if org.name == name:
                return org
        return None

    def get_pending_organizations(self) -> list[OrganizationEntity]:
        return [org for org in self.organizations.values() if org.status == OrganizationStatus.PENDING]


class InMemoryMembershipRepository(MembershipRepositoryInterface):
    def __init__(self):
        self.memberships: dict[uuid.UUID, MembershipEntity] = {}

    def save(self, entity: MembershipEntity) -> MembershipEntity:
        self.memberships[entity.id] = entity
        return entity

    def find_by_id(self, id: uuid.UUID) -> MembershipEntity | None:
        return self.memberships.get(id)

    def delete(self, id: uuid.UUID) -> None:
        if id in self.memberships:
            del self.memberships[id]

    def find_all(self, offset: int = 0, limit: int = 20) -> list[MembershipEntity]:
        return list(self.memberships.values())[offset : offset + limit]

    def count(self) -> int:
        return len(self.memberships)

    def find_by_user_and_organization(self, user_id: uuid.UUID, organization_id: uuid.UUID) -> MembershipEntity | None:
        for mem in self.memberships.values():
            if mem.user_id == user_id and mem.organization_id == organization_id:
                return mem
        return None

    def get_user_memberships(self, user_id: uuid.UUID) -> list[MembershipEntity]:
        return [mem for mem in self.memberships.values() if mem.user_id == user_id]

    def get_organization_members(self, organization_id: uuid.UUID) -> list[MembershipEntity]:
        return [mem for mem in self.memberships.values() if mem.organization_id == organization_id]
