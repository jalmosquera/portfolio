from rest_framework.routers import DefaultRouter
from .views import ProjectImage

router = DefaultRouter()
router.register(r"projectImage", ProjectImages, basename="projectImage")

urlpatterns = router.urls

