"""
Router configuration for the about app API.
Configuración del router para la API de la app about.
"""

from rest_framework.routers import DefaultRouter
from .views import AboutMeViewSet

router = DefaultRouter()
router.register(r'about', AboutMeViewSet, basename='about')

urlpatterns = router.urls
