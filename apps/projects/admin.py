"""
Projects app admin configuration.
Configuración de admin para la app projects.
"""

from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin configuration for Project model."""

    list_display = ["title", "is_featured", "order", "created_at"]
    list_filter = ["is_featured", "created_at"]
    search_fields = ["title", "description", "technologies"]
    list_editable = ["is_featured", "order"]
    ordering = ["order", "-created_at"]

    fieldsets = (
        ("Basic Information", {
            "fields": ("title", "short_description", "description")
        }),
        ("Media", {
            "fields": ("image",)
        }),
        ("Links", {
            "fields": ("url", "github_url")
        }),
        ("Technical Details", {
            "fields": ("technologies",)
        }),
        ("Display Options", {
            "fields": ("is_featured", "order")
        }),
    )
