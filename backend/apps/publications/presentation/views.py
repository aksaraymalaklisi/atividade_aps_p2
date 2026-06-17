from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from apps.publications.application.strategies import LocalFileSystemImageStorageStrategy
from apps.publications.application.use_cases.create_publication import CreatePublicationUseCase
from apps.publications.application.use_cases.list_publications import ListPublicationsUseCase
from apps.publications.domain.value_objects import PublicationStatus
from apps.publications.infrastructure.repositories import DjangoPublicationRepository
from apps.publications.models import Publication
from apps.publications.presentation.serializers import CreatePublicationSerializer, PublicationSerializer


class PublicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Publications.
    Supports listing (with filters/search) and creation.
    """
    queryset = Publication.objects.select_related("pet", "organization", "publisher").prefetch_related("pet__images").all()
    serializer_class = PublicationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        'status': ['exact'],
        'pet__species': ['exact', 'icontains'],
        'pet__size': ['exact'],
        'pet__gender': ['exact'],
        'organization_id': ['exact'],
    }
    search_fields = ['pet__name', 'pet__breed', 'pet__description']
    ordering_fields = ['created_at', 'pet__approximate_age']
    ordering = ['-created_at']

    def get_queryset(self):
        # Always return ACTIVE publications by default unless filtered otherwise
        qs = super().get_queryset()
        if 'status' not in self.request.query_params:
            qs = qs.filter(status=PublicationStatus.ACTIVE.value)
        return qs

    def create(self, request, *args, **kwargs):
        # We use a custom serializer for input to handle the multi-part file upload
        serializer = CreatePublicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        dto = serializer.to_dto(user_id=request.user.id)
        
        # Instantiate use case (in a real app, use Dependency Injection container)
        repo = DjangoPublicationRepository()
        strategy = LocalFileSystemImageStorageStrategy()
        use_case = CreatePublicationUseCase(repository=repo, image_strategy=strategy)
        
        result = use_case.execute(dto)
        
        # Return the created publication full data
        created_pub = self.get_queryset().get(id=result.publication_id)
        out_serializer = self.get_serializer(created_pub)
        
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)
