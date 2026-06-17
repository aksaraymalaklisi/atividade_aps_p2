from behave import given, then, when
from django.urls import reverse
from rest_framework.test import APIClient

from apps.accounts.infrastructure.models import User

# This will be run using behave-django, so the database is automatically available.


@given('I have a valid email "{email}" and username "{username}"')  # type: ignore
def step_impl_valid_email_username(context, email, username):
    if not hasattr(context, "api_client"):
        context.api_client = APIClient()
    context.register_payload = {"email": email, "username": username}


@given('a secure password "{password}"')  # type: ignore
def step_impl_secure_password(context, password):
    context.register_payload["password"] = password


@when("I submit the registration form")  # type: ignore
def step_impl_submit_registration(context):
    url = reverse("accounts:register")
    context.response = context.api_client.post(url, context.register_payload, format="json")


@then("I should receive a successful response with status {status_code:d}")  # type: ignore
def step_impl_successful_response(context, status_code):
    assert context.response.status_code == status_code, f"Expected {status_code}, got {context.response.status_code}"


@then("my new user account should be created in the system")  # type: ignore
def step_impl_account_created(context):
    email = context.register_payload["email"]
    assert User.objects.filter(email=email).exists(), "User was not created in DB."


@given('a user already exists with email "{email}" and username "{username}"')  # type: ignore
def step_impl_user_exists(context, email, username):
    if not hasattr(context, "api_client"):
        context.api_client = APIClient()
    User.objects.create_user(email=email, username=username, password="DummyPassword123!")


@when('I submit the registration form with email "{email}" and username "{username}"')  # type: ignore
def step_impl_submit_registration_duplicate(context, email, username):
    url = reverse("accounts:register")
    payload = {"email": email, "username": username, "password": "DummyPassword123!"}
    context.response = context.api_client.post(url, payload, format="json")


@then("I should receive an error response with status {status_code:d}")  # type: ignore
def step_impl_error_response(context, status_code):
    assert context.response.status_code == status_code, f"Expected {status_code}, got {context.response.status_code}"


@then('the error code should be "{error_code}"')  # type: ignore
def step_impl_error_code(context, error_code):
    assert context.response.data.get("code") == error_code, f"Expected {error_code}, got {context.response.data.get('code')}"


@given('a user already exists with email "{email}" and password "{password}"')  # type: ignore
def step_impl_user_exists_with_password(context, email, password):
    if not hasattr(context, "api_client"):
        context.api_client = APIClient()
    User.objects.create_user(email=email, username="login_user", password=password)


@when('I submit the login form with email "{email}" and password "{password}"')  # type: ignore
def step_impl_submit_login(context, email, password):
    url = reverse("accounts:login")
    payload = {"email": email, "password": password}
    context.response = context.api_client.post(url, payload, format="json")


@then("the response should contain access and refresh JWT tokens")  # type: ignore
def step_impl_contains_tokens(context):
    data = context.response.data
    assert "access" in data, "No access token in response"
    assert "refresh" in data, "No refresh token in response"
