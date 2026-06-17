import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.infrastructure.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def make_user(email="test@example.com", username="testuser", password="Password123!"):
        user = User(email=email, username=username)
        user.set_password(password)
        user.save()
        return user
    return make_user


@pytest.mark.django_db
def test_register_user_api_success(api_client):
    url = reverse("accounts:register")
    data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "SecurePassword123!",
        "first_name": "New",
        "last_name": "User",
    }

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.data
    assert response.data["email"] == "newuser@example.com"
    assert response.data["username"] == "newuser"

    # Verify in DB
    assert User.objects.filter(email="newuser@example.com").exists()


@pytest.mark.django_db
def test_register_user_api_duplicate_fails(api_client, create_user):
    create_user(email="existing@example.com", username="existing")

    url = reverse("accounts:register")
    data = {
        "email": "existing@example.com",
        "username": "another_username",
        "password": "SecurePassword123!",
    }

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["code"] == "USER_ALREADY_EXISTS"


@pytest.mark.django_db
def test_login_api_success(api_client, create_user):
    create_user(email="login@example.com", username="loginuser", password="Password123!")

    url = reverse("accounts:login")
    data = {
        "email": "login@example.com",
        "password": "Password123!",
    }

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data
    assert response.data["user"]["email"] == "login@example.com"


@pytest.mark.django_db
def test_login_api_wrong_password_fails(api_client, create_user):
    create_user(email="login@example.com", username="loginuser", password="Password123!")

    url = reverse("accounts:login")
    data = {
        "email": "login@example.com",
        "password": "WrongPassword!",
    }

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["code"] == "INVALID_CREDENTIALS"


@pytest.mark.django_db
def test_profile_api_success(api_client, create_user):
    user = create_user()

    # Authenticate
    api_client.force_authenticate(user=user)

    url = reverse("accounts:profile")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == user.email


@pytest.mark.django_db
def test_profile_api_unauthorized_fails(api_client):
    url = reverse("accounts:profile")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
