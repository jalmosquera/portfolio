"""
ASGI config for portfolio project.
Configuración ASGI para el proyecto portfolio.

It exposes the ASGI callable as a module-level variable named ``application``.
Expone el callable ASGI como una variable a nivel de módulo llamada ``application``.

For more information on this file, see
Para más información sobre este archivo, ver
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = get_asgi_application()
