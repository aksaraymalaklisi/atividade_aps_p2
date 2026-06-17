from rest_framework import serializers

from apps.organizations.models import Membership, Organization


class OrganizationSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()

    class Meta:  # type: ignore
        model = Organization
        fields = ("id", "name", "cnpj", "email", "phone", "address", "description", "document_url", "status", "created_at", "is_owner")
        read_only_fields = ("id", "document_url", "status", "created_at", "is_owner")

    def get_is_owner(self, obj) -> bool:
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.members.filter(user=request.user, role="OWNER").exists()
        return False


class RegisterOrganizationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    cnpj = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    address = serializers.CharField(max_length=500)
    description = serializers.CharField()
    document = serializers.FileField()


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore
        model = Membership
        fields = ("id", "user", "organization", "role", "created_at")
        read_only_fields = ("id", "created_at")


class RejectOrganizationSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=500)
