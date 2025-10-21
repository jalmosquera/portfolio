"""
About app configuration.
Configuración de la app about.
"""

from django.apps import AppConfig


class AboutConfig(AppConfig):
    """About app config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.about'
