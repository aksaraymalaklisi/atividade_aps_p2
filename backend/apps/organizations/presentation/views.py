import uuid

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.organizations.application.commands import (
    ApproveOrganizationCommand,
    RejectOrganizationCommand,
)
from apps.organizations.application.strategies import LocalFileSystemStorageStrategy
from apps.organizations.application.use_cases.register_organization import (
    RegisterOrganizationInputDTO,
    RegisterOrganizationUseCase,
)
from apps.organizations.infrastructure.repositories import (
    DjangoMembershipRepository,
    DjangoOrganizationRepository,
)
from apps.organizations.models import Organization
from apps.organizations.presentation.permissions import IsOperator
from apps.organizations.presentation.serializers import (
    OrganizationSerializer,
    RegisterOrganizationSerializer,
    RejectOrganizationSerializer,
)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = RegisterOrganizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        repo_org = DjangoOrganizationRepository()
        repo_mem = DjangoMembershipRepository()
        strategy = LocalFileSystemStorageStrategy()

        use_case = RegisterOrganizationUseCase(repo_org, repo_mem, strategy)

        file_obj = serializer.validated_data["document"]

        try:
            input_dto = RegisterOrganizationInputDTO(
                name=serializer.validated_data["name"],
                cnpj=serializer.validated_data["cnpj"],
                email=serializer.validated_data["email"],
                phone=serializer.validated_data.get("phone", ""),
                address=serializer.validated_data["address"],
                description=serializer.validated_data["description"],
                owner_user_id=request.user.id,
                document_name=file_obj.name,
                document_content=file_obj,
            )
            result = use_case.execute(input_dto)
            return Response(
                {
                    "organization_id": result.organization_id,
                    "status": result.status,
                    "document_url": result.document_url,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsOperator])
    def approve(self, request, pk=None):
        """Operator only: Approve organization"""
        if not pk:
            return Response({"error": "Organization ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            org_id = uuid.UUID(str(pk))
        except ValueError:
            return Response({"error": "Invalid UUID format."}, status=status.HTTP_400_BAD_REQUEST)

        repo_org = DjangoOrganizationRepository()

        command = ApproveOrganizationCommand(
            organization_id=org_id, 
            operator_id=request.user.id,  # type: ignore
            repository=repo_org
        )

        try:
            command.execute()
            return Response({"detail": "Organization approved successfully."})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsOperator])
    def reject(self, request, pk=None):
        """Operator only: Reject organization"""
        if not pk:
            return Response({"error": "Organization ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            org_id = uuid.UUID(str(pk))
        except ValueError:
            return Response({"error": "Invalid UUID format."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RejectOrganizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        repo_org = DjangoOrganizationRepository()

        command = RejectOrganizationCommand(
            organization_id=org_id,
            operator_id=request.user.id,  # type: ignore
            reason=serializer.validated_data["reason"],
            repository=repo_org,
        )

        try:
            command.execute()
            return Response({"detail": "Organization rejected successfully."})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
