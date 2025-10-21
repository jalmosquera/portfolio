"""
Router configuration for the projects app API.
Configuración del router para la API de la app projects.
"""

from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = router.urls
