import uuid

from apps.organizations.domain.entities import MembershipEntity, OrganizationEntity
from apps.organizations.domain.repositories import (
    MembershipRepositoryInterface,
    OrganizationRepositoryInterface,
)
from apps.organizations.domain.value_objects import MembershipRole, OrganizationStatus
from apps.organizations.models import Membership, Organization


class DjangoOrganizationRepository(OrganizationRepositoryInterface):
    def save(self, entity: OrganizationEntity) -> OrganizationEntity:
        Organization.objects.update_or_create(
            id=entity.id,
            defaults={
                "name": entity.name,
                "cnpj": entity.cnpj,
                "email": entity.email,
                "phone": entity.phone,
                "address": entity.address,
                "description": entity.description,
                "document_url": entity.document_url,
                "status": entity.status.value,
                "created_at": entity.created_at,
                "updated_at": entity.updated_at,
            },
        )
        return entity

    def find_by_id(self, id: uuid.UUID) -> OrganizationEntity | None:
        try:
            model = Organization.objects.get(id=id)
            return OrganizationEntity(
                id=model.id,
                name=model.name,
                cnpj=model.cnpj,
                email=model.email,
                phone=model.phone,
                address=model.address,
                description=model.description,
                document_url=model.document_url,
                status=OrganizationStatus(model.status),
                created_at=model.created_at,
                updated_at=model.updated_at,
            )
        except Organization.DoesNotExist:
            return None

    def delete(self, id: uuid.UUID) -> None:
        Organization.objects.filter(id=id).delete()

    def find_all(self, offset: int = 0, limit: int = 20) -> list[OrganizationEntity]:
        models = Organization.objects.all()[offset : offset + limit]
        return [
            OrganizationEntity(
                id=m.id,
                name=m.name,
                cnpj=m.cnpj,
                email=m.email,
                phone=m.phone,
                address=m.address,
                description=m.description,
                document_url=m.document_url,
                status=OrganizationStatus(m.status),
                created_at=m.created_at,
                updated_at=m.updated_at,
            )
            for m in models
        ]

    def count(self) -> int:
        return Organization.objects.count()

    def find_by_name(self, name: str) -> OrganizationEntity | None:
        try:
            model = Organization.objects.get(name=name)
            return OrganizationEntity(
                id=model.id,
                name=model.name,
                cnpj=model.cnpj,
                email=model.email,
                phone=model.phone,
                address=model.address,
                description=model.description,
                document_url=model.document_url,
                status=OrganizationStatus(model.status),
                created_at=model.created_at,
                updated_at=model.updated_at,
            )
        except Organization.DoesNotExist:
            return None

    def get_pending_organizations(self) -> list[OrganizationEntity]:
        models = Organization.objects.filter(status=OrganizationStatus.PENDING.value)
        return [
            OrganizationEntity(
                id=m.id,
                name=m.name,
                cnpj=m.cnpj,
                email=m.email,
                phone=m.phone,
                address=m.address,
                description=m.description,
                document_url=m.document_url,
                status=OrganizationStatus(m.status),
                created_at=m.created_at,
                updated_at=m.updated_at,
            )
            for m in models
        ]


class DjangoMembershipRepository(MembershipRepositoryInterface):
    def save(self, entity: MembershipEntity) -> MembershipEntity:
        Membership.objects.update_or_create(
            id=entity.id,
            defaults={
                "user_id": entity.user_id,
                "organization_id": entity.organization_id,
                "role": entity.role.value,
                "created_at": entity.created_at,
            },
        )
        return entity

    def find_by_id(self, id: uuid.UUID) -> MembershipEntity | None:
        try:
            model = Membership.objects.get(id=id)
            return MembershipEntity(
                id=model.id,
                user_id=model.user_id,
                organization_id=model.organization_id,
                role=MembershipRole(model.role),
                created_at=model.created_at,
            )
        except Membership.DoesNotExist:
            return None

    def delete(self, id: uuid.UUID) -> None:
        Membership.objects.filter(id=id).delete()

    def find_all(self, offset: int = 0, limit: int = 20) -> list[MembershipEntity]:
        models = Membership.objects.all()[offset : offset + limit]
        return [
            MembershipEntity(
                id=m.id,
                user_id=m.user_id,
                organization_id=m.organization_id,
                role=MembershipRole(m.role),
                created_at=m.created_at,
            )
            for m in models
        ]

    def count(self) -> int:
        return Membership.objects.count()

    def find_by_user_and_organization(self, user_id: uuid.UUID, organization_id: uuid.UUID) -> MembershipEntity | None:
        try:
            model = Membership.objects.get(user_id=user_id, organization_id=organization_id)
            return MembershipEntity(
                id=model.id,
                user_id=model.user_id,
                organization_id=model.organization_id,
                role=MembershipRole(model.role),
                created_at=model.created_at,
            )
        except Membership.DoesNotExist:
            return None

    def get_user_memberships(self, user_id: uuid.UUID) -> list[MembershipEntity]:
        models = Membership.objects.filter(user_id=user_id)
        return [
            MembershipEntity(
                id=m.id,
                user_id=m.user_id,
                organization_id=m.organization_id,
                role=MembershipRole(m.role),
                created_at=m.created_at,
            )
            for m in models
        ]

    def get_organization_members(self, organization_id: uuid.UUID) -> list[MembershipEntity]:
        models = Membership.objects.filter(organization_id=organization_id)
        return [
            MembershipEntity(
                id=m.id,
                user_id=m.user_id,
                organization_id=m.organization_id,
                role=MembershipRole(m.role),
                created_at=m.created_at,
            )
            for m in models
        ]
