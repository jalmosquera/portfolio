"""
Router configuration for the skills app API.
Configuración del router para la API de la app skills.
"""

from rest_framework.routers import DefaultRouter
from .views import SkillViewSet, SkillCategoryViewSet

router = DefaultRouter()
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'skill-categories', SkillCategoryViewSet, basename='skill-category')

urlpatterns = router.urls
