"""
Base entity class for all domain entities.

Domain entities are plain Python objects (POPOs) that represent the core
business concepts. They are completely independent of Django, ORM, or any
framework — ensuring the domain layer has zero external dependencies.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class BaseEntity:
    """
    Base class for all domain entities.

    Provides a UUID-based identity and creation timestamp.
    Subclasses should add their own domain-specific fields.
    """

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseEntity):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
