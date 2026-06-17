from rest_framework import serializers

from apps.organizations.presentation.serializers import OrganizationSerializer
from apps.publications.application.dtos import CreatePublicationInputDTO
from apps.publications.domain.value_objects import PetGender, PetSize
from apps.publications.models import Pet, PetImage, Publication


class PetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetImage
        fields = ["id", "image", "is_primary", "order"]


class PetSerializer(serializers.ModelSerializer):
    images = PetImageSerializer(many=True, read_only=True)

    class Meta:
        model = Pet
        fields = [
            "id",
            "name",
            "species",
            "breed",
            "size",
            "gender",
            "approximate_age",
            "description",
            "vaccinated",
            "neutered",
            "images",
        ]


class PublicationSerializer(serializers.ModelSerializer):
    pet = PetSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)
    publisher_name = serializers.CharField(source="publisher.first_name", read_only=True)
    can_edit = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = [
            "id",
            "publisher_id",
            "publisher_name",
            "organization_id",
            "organization",
            "status",
            "created_at",
            "updated_at",
            "pet",
            "can_edit",
        ]

    def get_can_edit(self, obj) -> bool:
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        if obj.publisher_id == request.user.id:
            return True
        if obj.organization_id:
            return request.user.memberships.filter(organization_id=obj.organization_id).exists()
        return False


class CreatePublicationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    species = serializers.CharField(max_length=100)
    breed = serializers.CharField(max_length=100, allow_blank=True, required=False)
    size = serializers.ChoiceField(choices=[(s.value, s.name) for s in PetSize])
    gender = serializers.ChoiceField(choices=[(g.value, g.name) for g in PetGender])
    approximate_age = serializers.IntegerField(min_value=0)
    description = serializers.CharField(allow_blank=True, required=False)
    vaccinated = serializers.BooleanField(default=False)
    neutered = serializers.BooleanField(default=False)
    organization_id = serializers.UUIDField(required=False, allow_null=True)
    images = serializers.ListField(
        child=serializers.ImageField(),
        max_length=5,
        allow_empty=False,
    )

    def to_dto(self, user_id) -> CreatePublicationInputDTO:
        data = self.validated_data
        return CreatePublicationInputDTO(
            publisher_id=user_id,
            name=data["name"],
            species=data["species"],
            breed=data.get("breed", ""),
            size=data["size"],
            gender=data["gender"],
            approximate_age=data["approximate_age"],
            description=data.get("description", ""),
            vaccinated=data.get("vaccinated", False),
            neutered=data.get("neutered", False),
            organization_id=data.get("organization_id"),
            images=data["images"],
        )


class UpdatePublicationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    species = serializers.CharField(max_length=100, required=False)
    breed = serializers.CharField(max_length=100, allow_blank=True, required=False)
    size = serializers.ChoiceField(choices=[(s.value, s.name) for s in PetSize], required=False)
    gender = serializers.ChoiceField(choices=[(g.value, g.name) for g in PetGender], required=False)
    approximate_age = serializers.IntegerField(min_value=0, required=False)
    description = serializers.CharField(allow_blank=True, required=False)
    vaccinated = serializers.BooleanField(default=False, required=False)
    neutered = serializers.BooleanField(default=False, required=False)
    images = serializers.ListField(
        child=serializers.ImageField(),
        max_length=5,
        allow_empty=True,
        required=False,
    )
