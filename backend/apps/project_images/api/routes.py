from rest_framework.routers import DefaultRouter
from .views import ProjectImageViewSet

router = DefaultRouter()
router.register(r"project-images", ProjectImageViewSet, basename="project-image")

urlpatterns = router.urls
