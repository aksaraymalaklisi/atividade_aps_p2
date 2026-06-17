import uuid

from apps.organizations.domain.entities import MembershipEntity, OrganizationEntity
from core.base_repository import Repository


class OrganizationRepositoryInterface(Repository[OrganizationEntity]):
    """
    Interface for Organization Repository.
    Extends BaseRepository for generic CRUD operations.
    """

    def find_by_name(self, name: str) -> OrganizationEntity | None:
        """Find an organization by its name."""
        pass

    def get_pending_organizations(self) -> list[OrganizationEntity]:
        """Retrieve all organizations with PENDING status."""
        pass


class MembershipRepositoryInterface(Repository[MembershipEntity]):
    """
    Interface for Membership Repository.
    """

    def find_by_user_and_organization(self, user_id: uuid.UUID, organization_id: uuid.UUID) -> MembershipEntity | None:
        """Find a specific membership record."""
        pass

    def get_user_memberships(self, user_id: uuid.UUID) -> list[MembershipEntity]:
        """Retrieve all memberships for a specific user."""
        pass

    def get_organization_members(self, organization_id: uuid.UUID) -> list[MembershipEntity]:
        """Retrieve all memberships for a specific organization."""
        pass
