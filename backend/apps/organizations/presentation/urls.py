from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.organizations.presentation.views import OrganizationViewSet

app_name = "organizations"

router = DefaultRouter()
router.register(r"", OrganizationViewSet, basename="organization")

urlpatterns = [
    path("", include(router.urls)),
]
