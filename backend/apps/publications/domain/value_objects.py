from enum import Enum


class PublicationStatus(Enum):
    ACTIVE = "ACTIVE"
    ADOPTED = "ADOPTED"
    REMOVED = "REMOVED"


class PetSize(Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"


class PetGender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    UNKNOWN = "UNKNOWN"
