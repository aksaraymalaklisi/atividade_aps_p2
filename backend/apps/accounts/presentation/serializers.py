from rest_framework import serializers

from apps.accounts.application.dtos import AuthenticateUserInput, RegisterUserInput


class RegisterUserRequestSerializer(serializers.Serializer):
    """Serializer for validating user registration input."""

    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    show_phone = serializers.BooleanField(default=False)

    def to_dto(self) -> RegisterUserInput:
        return RegisterUserInput(**self.validated_data)


class UserResponseSerializer(serializers.Serializer):
    """Serializer for user output representation."""

    id = serializers.UUIDField()
    email = serializers.EmailField()
    username = serializers.CharField()


class AuthenticateUserRequestSerializer(serializers.Serializer):
    """Serializer for validating login input."""

    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if not attrs.get("email") and not attrs.get("username"):
            raise serializers.ValidationError("Either email or username is required.")
        return attrs

    def to_dto(self) -> AuthenticateUserInput:
        return AuthenticateUserInput(
            email=self.validated_data.get("email"),
            username=self.validated_data.get("username"),
            password=self.validated_data["password"],
        )


class TokenResponseSerializer(serializers.Serializer):
    """Serializer for returning JWT tokens + user info."""

    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserResponseSerializer()
