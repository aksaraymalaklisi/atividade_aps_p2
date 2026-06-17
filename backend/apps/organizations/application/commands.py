import uuid
from abc import ABC, abstractmethod

from apps.organizations.application.observers import AuditEvent, audit_subject
from apps.organizations.domain.repositories import OrganizationRepositoryInterface


class Command(ABC):
    """
    The Command interface declares a method for executing a command.
    """

    @abstractmethod
    def execute(self) -> None:
        pass


class ApproveOrganizationCommand(Command):
    """
    Command to approve a pending organization.
    Only Operators should invoke this (checked at the Presentation layer).
    """

    def __init__(
        self,
        organization_id: uuid.UUID,
        operator_id: uuid.UUID,
        repository: OrganizationRepositoryInterface,
    ):
        self.organization_id = organization_id
        self.operator_id = operator_id
        self.repository = repository

    def execute(self) -> None:
        organization = self.repository.find_by_id(self.organization_id)
        if not organization:
            raise ValueError(f"Organization with id {self.organization_id} not found.")

        if organization.is_approved():
            raise ValueError(f"Organization {organization.name} is already approved.")

        # Realiza a aprovação na entidade de domínio
        organization.approve()

        # Salva as mudanças
        self.repository.save(organization)

        # Dispara evento para o Audit Log (Observer Pattern)
        audit_subject.notify(
            AuditEvent(
                event_type="ORGANIZATION_APPROVED",
                payload={
                    "organization_id": str(organization.id),
                    "operator_id": str(self.operator_id),
                    "status": organization.status.value,
                },
            )
        )


class RejectOrganizationCommand(Command):
    """
    Command to reject a pending organization.
    """

    def __init__(
        self,
        organization_id: uuid.UUID,
        operator_id: uuid.UUID,
        reason: str,
        repository: OrganizationRepositoryInterface,
    ):
        self.organization_id = organization_id
        self.operator_id = operator_id
        self.reason = reason
        self.repository = repository

    def execute(self) -> None:
        organization = self.repository.find_by_id(self.organization_id)
        if not organization:
            raise ValueError(f"Organization with id {self.organization_id} not found.")

        # Realiza a rejeição na entidade de domínio
        organization.reject()

        # Salva as mudanças
        self.repository.save(organization)

        # Dispara evento para o Audit Log
        audit_subject.notify(
            AuditEvent(
                event_type="ORGANIZATION_REJECTED",
                payload={
                    "organization_id": str(organization.id),
                    "operator_id": str(self.operator_id),
                    "reason": self.reason,
                    "status": organization.status.value,
                },
            )
        )
