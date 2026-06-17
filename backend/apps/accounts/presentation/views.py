from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.application.use_cases.authenticate_user import AuthenticateUserUseCase
from apps.accounts.application.use_cases.register_user import RegisterUserUseCase
from apps.accounts.infrastructure.repositories import DjangoUserRepository
from apps.accounts.infrastructure.services import DjangoPasswordHashService
from apps.accounts.presentation.serializers import (
    AuthenticateUserRequestSerializer,
    RegisterUserRequestSerializer,
    TokenResponseSerializer,
    UserResponseSerializer,
)
from core.exceptions import ApplicationError


class RegisterUserView(APIView):
    """API Endpoint for user registration."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterUserRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = RegisterUserUseCase(user_repository=DjangoUserRepository())

        try:
            output_dto = use_case.execute(serializer.to_dto())
            # We can reuse UserResponseSerializer to format the output
            response_data = UserResponseSerializer(output_dto).data
            return Response(response_data, status=status.HTTP_201_CREATED)
        except ApplicationError as e:
            # Handle domain errors like UserAlreadyExistsError
            return Response({"detail": e.message, "code": e.code}, status=status.HTTP_400_BAD_REQUEST)


class AuthenticateUserView(APIView):
    """API Endpoint for user login (returns JWT tokens)."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AuthenticateUserRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = AuthenticateUserUseCase(
            user_repository=DjangoUserRepository(),
            hash_service=DjangoPasswordHashService(),
        )

        try:
            output_dto = use_case.execute(serializer.to_dto())

            # Generate JWT tokens. Since we are bypassing Django's authenticate(),
            # we need to generate tokens for the Django User object manually.
            # In Clean Architecture, infrastructure bridges this gap.
            from apps.accounts.infrastructure.models import User as DjangoUser
            django_user = DjangoUser.objects.get(id=output_dto.id)

            refresh = RefreshToken.for_user(django_user)

            response_data = TokenResponseSerializer({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": output_dto,
            }).data

            return Response(response_data, status=status.HTTP_200_OK)

        except ApplicationError as e:
            return Response({"detail": e.message, "code": e.code}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(APIView):
    """API Endpoint for fetching the current user's profile."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # DRF sets request.user to the Django User model instance
        user = request.user
        response_data = UserResponseSerializer(user).data
        return Response(response_data, status=status.HTTP_200_OK)
