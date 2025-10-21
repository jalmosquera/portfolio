"""
URL configuration for portfolio project.
Configuración de URL para el proyecto portfolio.

The `urlpatterns` list routes URLs to views. For more information please see:
La lista `urlpatterns` enruta URLs a vistas. Para más información ver:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Admin site
    path("admin/", admin.site.urls),

    # API Documentation - Documentación de API
    # Root page is Redoc documentation - La página raíz es la documentación Redoc
    path("", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # API endpoints
    path("api/", include("apps.projects.api.router")),
    path("api/", include("apps.skills.api.router")),
    path("api/", include("apps.about.api.router")),
    path("api/", include("apps.contact.api.router")),
]

# Serve media files in development
# Servir archivos multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
