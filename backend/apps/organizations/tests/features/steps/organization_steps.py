import uuid
from behave import given, when, then
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from apps.organizations.models import Organization, Membership
from apps.organizations.domain.value_objects import OrganizationStatus, MembershipRole

User = get_user_model()


@given('a logged in user with email "{email}"')  # type: ignore
def step_given_logged_in_user(context, email):
    context.user = User.objects.create_user(username=email.split("@")[0], email=email, password="password123")  # type: ignore
    context.client = APIClient()
    context.client.force_authenticate(user=context.user)


@when('the user submits a registration for an organization named "{org_name}"')  # type: ignore
def step_when_register_organization(context, org_name):
    # Simulando o upload do arquivo base64 ou mock
    data = {
        "name": org_name,
        "cnpj": "00.000.000/0000-00",
        "email": "org@test.com",
        "phone": "11999999999",
        "address": "Test Address",
        "description": "NGO Description",
    }
    
    # Criaremos o mock do arquivo para não quebrar a view real
    from django.core.files.uploadedfile import SimpleUploadedFile
    mock_file = SimpleUploadedFile("doc.pdf", b"file_content", content_type="application/pdf")
    data["document"] = mock_file

    response = context.client.post("/api/v1/organizations/", data, format="multipart")
    context.response = response


@then('the organization should be created with status "{status}"')  # type: ignore
def step_then_organization_status(context, status):
    assert context.response.status_code == 201, context.response.data
    org_id = context.response.data["organization_id"]
    org = Organization.objects.get(id=org_id)
    assert org.status == status
    context.org = org


@then('the user should be the "{role}" of the organization')  # type: ignore
def step_then_user_is_owner(context, role):
    membership = Membership.objects.get(user=context.user, organization=context.org)
    assert membership.role == role


@given('a logged in operator with email "{email}"')  # type: ignore
def step_given_operator(context, email):
    context.operator = User.objects.create_user(username=email.split("@")[0], email=email, password="password123", is_staff=True)  # type: ignore
    context.client = APIClient()
    context.client.force_authenticate(user=context.operator)


@given('an existing pending organization named "{org_name}"')  # type: ignore
def step_given_pending_org(context, org_name):
    context.org = Organization.objects.create(
        name=org_name,
        description="Pending ONG desc",
        status=OrganizationStatus.PENDING.value
    )


@when('the operator approves the organization "{org_name}"')  # type: ignore
def step_when_approve_org(context, org_name):
    response = context.client.post(f"/api/v1/organizations/{context.org.id}/approve/")
    context.response = response


@when('the operator rejects the organization "{org_name}" with reason "{reason}"')  # type: ignore
def step_when_reject_org(context, org_name, reason):
    data = {"reason": reason}
    response = context.client.post(f"/api/v1/organizations/{context.org.id}/reject/", data)
    context.response = response


@then('the organization status should be "{status}"')  # type: ignore
def step_then_check_status(context, status):
    assert context.response.status_code == 200, context.response.data
    context.org.refresh_from_db()
    assert context.org.status == status
