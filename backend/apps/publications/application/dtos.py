import uuid
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CreatePublicationInputDTO:
    publisher_id: uuid.UUID
    name: str
    species: str
    breed: str
    size: str
    gender: str
    approximate_age: int
    description: str
    vaccinated: bool
    neutered: bool
    images: list[Any]  # Django InMemoryUploadedFile or similar
    organization_id: uuid.UUID | None = None


@dataclass(frozen=True)
class CreatePublicationOutputDTO:
    publication_id: uuid.UUID
    pet_id: uuid.UUID | None
    status: str
