"""
Skills app configuration.
Configuración de la app skills.
"""

from django.apps import AppConfig


class SkillsConfig(AppConfig):
    """Skills app config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.skills'
