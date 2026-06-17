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


@dataclass(frozen=True)
class UpdatePublicationInputDTO:
    publication_id: uuid.UUID
    name: str | None = None
    species: str | None = None
    breed: str | None = None
    size: str | None = None
    gender: str | None = None
    approximate_age: int | None = None
    description: str | None = None
    vaccinated: bool | None = None
    neutered: bool | None = None
    images: list[Any] | None = None


@dataclass(frozen=True)
class UpdatePublicationStatusInputDTO:
    publication_id: uuid.UUID
    status: str
