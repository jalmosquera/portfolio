"""
Projects app configuration.
Configuración de la app projects.
"""

from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    """Configuration class for Projects app."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.projects"
    verbose_name = "Projects"
