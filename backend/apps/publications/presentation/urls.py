from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.publications.presentation.views import PublicationViewSet

router = DefaultRouter()
router.register(r"", PublicationViewSet, basename="publication")

urlpatterns = [
    path("", include(router.urls)),
]
