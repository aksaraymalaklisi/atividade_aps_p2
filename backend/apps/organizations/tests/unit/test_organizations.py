import uuid
from io import BytesIO

import pytest

from apps.organizations.application.commands import (
    ApproveOrganizationCommand,
    RejectOrganizationCommand,
)
from apps.organizations.application.strategies import MockStorageStrategy
from apps.organizations.application.use_cases.register_organization import (
    RegisterOrganizationInputDTO,
    RegisterOrganizationUseCase,
)
from apps.organizations.domain.value_objects import MembershipRole, OrganizationStatus
from apps.organizations.tests.unit.in_memory_repositories import (
    InMemoryMembershipRepository,
    InMemoryOrganizationRepository,
)


@pytest.fixture
def repo_org():
    return InMemoryOrganizationRepository()


@pytest.fixture
def repo_mem():
    return InMemoryMembershipRepository()


@pytest.fixture
def mock_strategy():
    return MockStorageStrategy()


def test_register_organization(repo_org, repo_mem, mock_strategy):
    use_case = RegisterOrganizationUseCase(repo_org, repo_mem, mock_strategy)
    owner_id = uuid.uuid4()

    input_dto = RegisterOrganizationInputDTO(
        name="ONG Test",
        cnpj="00.000.000/0000-00",
        email="test@ong.com",
        phone="11999999999",
        address="Test Address",
        description="A test ONG",
        owner_user_id=owner_id,
        document_name="doc.pdf",
        document_content=BytesIO(b"test content"),
    )

    result = use_case.execute(input_dto)

    assert result.status == OrganizationStatus.PENDING.value
    assert result.document_url == "http://mock-storage.com/documents/doc.pdf"

    org = repo_org.find_by_id(result.organization_id)
    assert org is not None
    assert org.name == "ONG Test"

    mem = repo_mem.find_by_user_and_organization(owner_id, org.id)
    assert mem is not None
    assert mem.role == MembershipRole.OWNER


def test_register_duplicate_organization(repo_org, repo_mem, mock_strategy):
    use_case = RegisterOrganizationUseCase(repo_org, repo_mem, mock_strategy)
    owner_id = uuid.uuid4()

    input_dto = RegisterOrganizationInputDTO(
        name="ONG Duplicate",
        cnpj="00.000.000/0000-01",
        email="test2@ong.com",
        phone="11999999999",
        address="Test Address",
        description="A test ONG",
        owner_user_id=owner_id,
        document_name="doc.pdf",
        document_content=BytesIO(b"test content"),
    )
    use_case.execute(input_dto)

    with pytest.raises(ValueError, match="already exists"):
        use_case.execute(input_dto)


def test_approve_organization_command(repo_org, repo_mem, mock_strategy):
    # Setup
    use_case = RegisterOrganizationUseCase(repo_org, repo_mem, mock_strategy)
    owner_id = uuid.uuid4()
    input_dto = RegisterOrganizationInputDTO(
        name="ONG To Approve",
        cnpj="00.000.000/0000-02",
        email="test3@ong.com",
        phone="11999999999",
        address="Test Address",
        description="To approve",
        owner_user_id=owner_id,
        document_name="doc.pdf",
        document_content=BytesIO(b"content"),
    )
    result = use_case.execute(input_dto)
    org_id = result.organization_id

    operator_id = uuid.uuid4()
    command = ApproveOrganizationCommand(org_id, operator_id, repo_org)

    # Execute
    command.execute()

    # Assert
    org = repo_org.find_by_id(org_id)
    assert org.status == OrganizationStatus.APPROVED


def test_reject_organization_command(repo_org, repo_mem, mock_strategy):
    # Setup
    use_case = RegisterOrganizationUseCase(repo_org, repo_mem, mock_strategy)
    owner_id = uuid.uuid4()
    input_dto = RegisterOrganizationInputDTO(
        name="ONG To Reject",
        cnpj="00.000.000/0000-03",
        email="test4@ong.com",
        phone="11999999999",
        address="Test Address",
        description="To reject",
        owner_user_id=owner_id,
        document_name="doc.pdf",
        document_content=BytesIO(b"content"),
    )
    result = use_case.execute(input_dto)
    org_id = result.organization_id

    operator_id = uuid.uuid4()
    command = RejectOrganizationCommand(org_id, operator_id, "Missing docs", repo_org)

    # Execute
    command.execute()

    # Assert
    org = repo_org.find_by_id(org_id)
    assert org.status == OrganizationStatus.REJECTED
