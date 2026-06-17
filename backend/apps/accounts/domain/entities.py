"""
User domain entity.

Pure Python dataclass — no Django dependencies.
Represents the core business concept of a user in the system.
"""

from dataclasses import dataclass, field

from core.base_entity import BaseEntity


@dataclass
class UserEntity(BaseEntity):
    """Domain entity representing a platform user."""

    email: str = ""
    username: str = ""
    first_name: str = ""
    last_name: str = ""
    phone: str = ""
    show_phone: bool = False
    is_operator: bool = False
    is_active: bool = True

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()
