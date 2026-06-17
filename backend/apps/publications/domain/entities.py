import uuid
from dataclasses import dataclass, field
from datetime import datetime

from apps.publications.domain.value_objects import PetGender, PetSize, PublicationStatus
from core.base_entity import BaseEntity


@dataclass
class PetImageEntity(BaseEntity):
    pet_id: uuid.UUID | None = None
    image: str = ""
    is_primary: bool = False
    order: int = 0


@dataclass
class PetEntity(BaseEntity):
    publication_id: uuid.UUID | None = None
    name: str = ""
    species: str = ""
    breed: str = ""
    size: str = PetSize.MEDIUM.value
    gender: str = PetGender.UNKNOWN.value
    approximate_age: int = 0
    description: str = ""
    vaccinated: bool = False
    neutered: bool = False
    images: list[PetImageEntity] = field(default_factory=list)


@dataclass
class PublicationEntity(BaseEntity):
    publisher_id: uuid.UUID | None = None
    organization_id: uuid.UUID | None = None
    status: str = PublicationStatus.ACTIVE.value
    updated_at: datetime | None = None
    pet: PetEntity | None = None

    def mark_as_adopted(self) -> None:
        self.status = PublicationStatus.ADOPTED.value

    def mark_as_removed(self) -> None:
        self.status = PublicationStatus.REMOVED.value
