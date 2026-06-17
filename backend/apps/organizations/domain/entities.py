import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime

from apps.organizations.domain.value_objects import MembershipRole, OrganizationStatus
from core.base_entity import BaseEntity


@dataclass
class OrganizationEntity(BaseEntity):
    name: str = ""
    cnpj: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""
    description: str = ""
    document_url: str | None = None
    status: OrganizationStatus = OrganizationStatus.PENDING
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def approve(self) -> None:
        """Approves the organization."""
        self.status = OrganizationStatus.APPROVED
        self.updated_at = datetime.now(UTC)

    def reject(self) -> None:
        """Rejects the organization."""
        self.status = OrganizationStatus.REJECTED
        self.updated_at = datetime.now(UTC)

    def is_approved(self) -> bool:
        return self.status == OrganizationStatus.APPROVED


@dataclass
class MembershipEntity(BaseEntity):
    user_id: uuid.UUID = field(default_factory=uuid.uuid4)
    organization_id: uuid.UUID = field(default_factory=uuid.uuid4)
    role: MembershipRole = MembershipRole.MEMBER

    def is_owner(self) -> bool:
        return self.role == MembershipRole.OWNER

    def is_leader(self) -> bool:
        return self.role in (MembershipRole.OWNER, MembershipRole.LEADER)
