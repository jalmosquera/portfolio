from rest_framework.routers import DefaultRouter
from .views import TechDetailViewSet

router = DefaultRouter()
router.register(r"tech-details", TechDetailViewSet, basename="tech-detail")

urlpatterns = router.urls
