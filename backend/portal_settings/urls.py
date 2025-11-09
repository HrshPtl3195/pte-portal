# portal/urls.py
from django.contrib import admin
from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.views.static import serve as static_serve
from django.views.generic import TemplateView

from apps.core.views import PingView, ProtectedMeView

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

# Public API schema endpoint (the JSON/openapi document)
schema_urlpattern = path("api/schema/", SpectacularAPIView.as_view(), name="schema")

# Documentation UIs — only enabled in DEBUG or when explicitly allowed
docs_urlpatterns = []
if settings.DEBUG or getattr(settings, "ENABLE_API_DOCS", False):
    docs_urlpatterns = [
        path(
            "api/docs/swagger/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "api/docs/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
    ]

urlpatterns = [
    path("admin/", admin.site.urls),

    # core/test endpoints
    path("api/ping/", PingView.as_view(), name="api-ping"),
    path("api/me/", ProtectedMeView.as_view(), name="api-me"),

    # OpenAPI JSON
    schema_urlpattern,

    # Docs (conditional)
    *docs_urlpatterns,

    # API v1: include app routers. Each app should set app_name in its urls.py
    path("api/v1/test-engine/", include(("apps.test_engine.urls", "test_engine"), namespace="test_engine")),
    path("api/v1/accounts/", include(("apps.accounts.urls", "accounts"), namespace="accounts")),
    # ... add other api includes ABOVE the catch-all ...
]

# Serve static/media in development only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# -----------------------
# SAFE CATCH-ALL FALLBACK
# -----------------------
# Purpose: serve frontend files / SPA index for non-API, non-admin routes.
# IMPORTANT: this must come AFTER all api/ and admin/ paths above.

# Option A — Serve files from a built frontend directory (development only)
# Replace 'frontend_dist' with the actual path where your frontend build artifacts live.
# Example: BASE_DIR / "frontend" / "dist"
FRONTEND_DIST_DIR = getattr(settings, "FRONTEND_DIST_DIR", None)
if FRONTEND_DIST_DIR:
    # Only match paths that do NOT start with "api/" or "admin/"
    urlpatterns += [
        re_path(r'^(?!api/|admin/)(?P<path>.*)$', static_serve, {
            "document_root": str(FRONTEND_DIST_DIR),
            "show_indexes": False,
        }),
    ]
else:
    # Option B — SPA template fallback (recommended if you place index.html in templates/)
    # This will render the template named "index.html" for any non-api, non-admin path.
    # Ensure 'index.html' exists in your TEMPLATE DIRS.
    urlpatterns += [
        re_path(r'^(?!api/|admin/).*$', TemplateView.as_view(template_name="index.html"), name="spa-index"),
    ]
