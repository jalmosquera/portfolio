"""
WSGI config for portfolio project.
Configuración WSGI para el proyecto portfolio.

It exposes the WSGI callable as a module-level variable named ``application``.
Expone el callable WSGI como una variable a nivel de módulo llamada ``application``.

For more information on this file, see
Para más información sobre este archivo, ver
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = get_wsgi_application()
