from django.contrib.auth.hashers import check_password, make_password

from apps.accounts.domain.services import PasswordHashServiceInterface


class DjangoPasswordHashService(PasswordHashServiceInterface):
    """
    Implementation of PasswordHashServiceInterface using Django's built-in hashing.
    By default, Django uses PBKDF2 with SHA256 (which is highly secure).
    """

    def hash(self, raw_password: str) -> str:
        return make_password(raw_password)

    def verify(self, raw_password: str, hashed_password: str) -> bool:
        return check_password(raw_password, hashed_password)
