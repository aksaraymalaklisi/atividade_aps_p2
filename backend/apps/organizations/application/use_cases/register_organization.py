import uuid
from dataclasses import dataclass
from typing import BinaryIO

from apps.organizations.application.strategies import DocumentUploadStrategy
from apps.organizations.domain.entities import MembershipEntity, OrganizationEntity
from apps.organizations.domain.repositories import (
    MembershipRepositoryInterface,
    OrganizationRepositoryInterface,
)
from apps.organizations.domain.value_objects import MembershipRole
from core.base_use_case import BaseUseCase


@dataclass
class RegisterOrganizationInputDTO:
    name: str
    cnpj: str
    email: str
    phone: str
    address: str
    description: str
    owner_user_id: uuid.UUID
    document_name: str
    document_content: BinaryIO


@dataclass
class RegisterOrganizationOutputDTO:
    organization_id: uuid.UUID
    status: str
    document_url: str


class RegisterOrganizationUseCase(BaseUseCase[RegisterOrganizationInputDTO, RegisterOrganizationOutputDTO]):
    """
    Use case to register a new organization.
    Uses DocumentUploadStrategy to store the verification document.
    """

    def __init__(
        self,
        organization_repo: OrganizationRepositoryInterface,
        membership_repo: MembershipRepositoryInterface,
        upload_strategy: DocumentUploadStrategy,
    ):
        self.organization_repo = organization_repo
        self.membership_repo = membership_repo
        self.upload_strategy = upload_strategy

    def execute(self, input_dto: RegisterOrganizationInputDTO) -> RegisterOrganizationOutputDTO:
        # Check if name is already taken
        existing_org = self.organization_repo.find_by_name(input_dto.name)
        if existing_org:
            raise ValueError(f"Organization with name {input_dto.name} already exists.")

        # Execute Strategy to upload document
        document_url = self.upload_strategy.upload(input_dto.document_name, input_dto.document_content)

        # Create Organization Entity
        org_entity = OrganizationEntity(
            name=input_dto.name,
            cnpj=input_dto.cnpj,
            email=input_dto.email,
            phone=input_dto.phone,
            address=input_dto.address,
            description=input_dto.description,
            document_url=document_url,
        )
        self.organization_repo.save(org_entity)

        # Create Owner Membership
        membership = MembershipEntity(
            user_id=input_dto.owner_user_id,
            organization_id=org_entity.id,
            role=MembershipRole.OWNER,
        )
        self.membership_repo.save(membership)

        return RegisterOrganizationOutputDTO(
            organization_id=org_entity.id,
            status=org_entity.status.value,
            document_url=document_url,
        )
