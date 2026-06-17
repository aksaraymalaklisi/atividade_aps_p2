from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from apps.publications.application.strategies import LocalFileSystemImageStorageStrategy
from apps.publications.application.use_cases.create_publication import CreatePublicationUseCase
from apps.publications.domain.value_objects import PublicationStatus
from apps.publications.infrastructure.repositories import DjangoPublicationRepository
from apps.publications.models import Publication
from apps.publications.presentation.serializers import CreatePublicationSerializer, PublicationSerializer


class PublicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Publications.
    Supports listing (with filters/search), creation, updating, and deletion.
    """
    queryset = Publication.objects.select_related("pet", "organization", "publisher").prefetch_related("pet__images").all()
    serializer_class = PublicationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]  # type: ignore
    filterset_fields = {
        'status': ['exact', 'in'],
        'pet__species': ['exact', 'icontains'],
        'pet__size': ['exact'],
        'pet__gender': ['exact'],
        'organization_id': ['exact'],
    }
    search_fields = ['pet__name', 'pet__breed', 'pet__description']
    ordering_fields = ['created_at', 'pet__approximate_age']
    ordering = ['-created_at']

    def get_permissions(self):
        from apps.publications.presentation.permissions import IsPublicationOwnerOrOrgMember
        if self.action in ['update', 'partial_update', 'destroy', 'mark_adopted']:
            return [permissions.IsAuthenticated(), IsPublicationOwnerOrOrgMember()]
        return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()
        
        if self.action == 'list':
            if self.request.query_params.get('include_adopted') == 'true':
                qs = qs.filter(status__in=[PublicationStatus.ACTIVE.value, PublicationStatus.ADOPTED.value])
            elif 'status' not in self.request.query_params:
                qs = qs.filter(status=PublicationStatus.ACTIVE.value)
        else:
            # Allow fetching both ACTIVE and ADOPTED for detail actions
            qs = qs.filter(status__in=[PublicationStatus.ACTIVE.value, PublicationStatus.ADOPTED.value])
            
        return qs

    def create(self, request, *args, **kwargs):
        serializer = CreatePublicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dto = serializer.to_dto(user_id=request.user.id)

        repo = DjangoPublicationRepository()
        strategy = LocalFileSystemImageStorageStrategy()
        use_case = CreatePublicationUseCase(repository=repo, image_strategy=strategy)

        result = use_case.execute(dto)

        created_pub = self.get_queryset().get(id=result.publication_id)
        out_serializer = self.get_serializer(created_pub, context={'request': request})
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        from apps.publications.application.dtos import UpdatePublicationInputDTO
        from apps.publications.application.use_cases.update_publication import UpdatePublicationUseCase
        from apps.publications.presentation.serializers import UpdatePublicationSerializer

        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = UpdatePublicationSerializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        dto = UpdatePublicationInputDTO(
            publication_id=instance.id,
            name=data.get("name"),
            species=data.get("species"),
            breed=data.get("breed"),
            size=data.get("size"),
            gender=data.get("gender"),
            approximate_age=data.get("approximate_age"),
            description=data.get("description"),
            vaccinated=data.get("vaccinated"),
            neutered=data.get("neutered"),
            images=data.get("images"),
        )

        repo = DjangoPublicationRepository()
        strategy = LocalFileSystemImageStorageStrategy()
        use_case = UpdatePublicationUseCase(repository=repo, image_strategy=strategy)

        try:
            use_case.execute(dto)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        updated_pub = self.get_queryset().get(id=instance.id)
        out_serializer = self.get_serializer(updated_pub, context={'request': request})
        return Response(out_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        from apps.publications.application.use_cases.delete_publication import DeletePublicationUseCase

        instance = self.get_object()
        repo = DjangoPublicationRepository()
        use_case = DeletePublicationUseCase(repository=repo)

        try:
            use_case.execute(instance.id)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def mark_adopted(self, request, pk=None):
        from apps.publications.application.dtos import UpdatePublicationStatusInputDTO
        from apps.publications.application.use_cases.change_publication_status import ChangePublicationStatusUseCase

        instance = self.get_object()
        dto = UpdatePublicationStatusInputDTO(publication_id=instance.id, status=PublicationStatus.ADOPTED.name)

        repo = DjangoPublicationRepository()
        use_case = ChangePublicationStatusUseCase(repository=repo)

        try:
            use_case.execute(dto)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        updated_pub = self.get_queryset().get(id=instance.id)
        out_serializer = self.get_serializer(updated_pub, context={'request': request})
        return Response(out_serializer.data, status=status.HTTP_200_OK)
