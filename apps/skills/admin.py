"""
Skills app admin configuration.
Configuración de admin para la app skills.
"""

from django.contrib import admin
from .models import Skill, SkillCategory


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    """Admin configuration for SkillCategory model."""

    list_display = ["name", "order", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "description"]
    list_editable = ["order"]
    ordering = ["order", "name"]

    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "description")
        }),
        ("Display Options", {
            "fields": ("order",)
        }),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Admin configuration for Skill model."""

    list_display = ["name", "category", "proficiency", "percentage", "years_experience", "is_featured", "order"]
    list_filter = ["category", "proficiency", "is_featured", "created_at"]
    search_fields = ["name", "description"]
    list_editable = ["proficiency", "percentage", "is_featured", "order"]
    ordering = ["category__order", "order", "name"]

    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "category", "description")
        }),
        ("Proficiency", {
            "fields": ("proficiency", "percentage", "years_experience")
        }),
        ("Media", {
            "fields": ("icon",)
        }),
        ("Display Options", {
            "fields": ("is_featured", "order")
        }),
    )
