import uuid
import pytest
from apps.publications.domain.factories import PublicationFactory
from apps.publications.domain.value_objects import PetGender, PetSize, PublicationStatus

def test_publication_factory_creates_valid_publication_with_pet():
    publisher_id = uuid.uuid4()
    
    pub, pet = PublicationFactory.create_publication_with_pet(
        publisher_id=publisher_id,
        name="Rex",
        species="Cachorro",
        breed="Vira-lata",
        size=PetSize.MEDIUM.value,
        gender=PetGender.MALE.value,
        approximate_age=2,
        description="Muito dócil.",
        vaccinated=True,
        neutered=False,
    )
    
    assert pub.publisher_id == publisher_id
    assert pub.status == PublicationStatus.ACTIVE.value
    assert pub.pet is not None
    assert pet.name == "Rex"
    assert pet.species == "Cachorro"
    assert pet.vaccinated is True
