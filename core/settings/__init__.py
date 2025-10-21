"""
Settings package initialization.
Inicialización del paquete de configuración.

This module automatically imports the appropriate settings based on DJANGO_ENV.
Este módulo importa automáticamente la configuración apropiada basada en DJANGO_ENV.
"""

import os

# Determine which settings to use based on DJANGO_ENV environment variable
# Determinar qué configuración usar basada en la variable de entorno DJANGO_ENV
env = os.getenv("DJANGO_ENV", "development")

if env == "production":
    from .production import *
else:
    from .development import *
