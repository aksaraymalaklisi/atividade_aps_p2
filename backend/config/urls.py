"""
Root URL configuration for PetAdopt.

All API endpoints are namespaced under /api/v1/.
OpenAPI documentation is served at /api/docs/ and /api/schema/.
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve as static_serve
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # API v1
    path("api/v1/accounts/", include("apps.accounts.presentation.urls")),
    path("api/v1/organizations/", include("apps.organizations.presentation.urls")),
    path("api/v1/publications/", include("apps.publications.presentation.urls")),
    path("api/v1/chats/", include("apps.chat.presentation.urls")),
    # Health check
    path(
        "api/health/",
        lambda request: __import__("django.http", fromlist=["JsonResponse"]).JsonResponse({"status": "ok"}),
    ),
]

# In production, serve uploaded media files through Django if no external media server is configured.
urlpatterns += [
    path(
        "media/<path:path>",
        static_serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]
