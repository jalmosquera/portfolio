"""
Router configuration for the contact app API.
Configuración del router para la API de la app contact.
"""

from rest_framework.routers import DefaultRouter
from .views import ContactMessageViewSet

router = DefaultRouter()
router.register(r'contact', ContactMessageViewSet, basename='contact')

urlpatterns = router.urls
