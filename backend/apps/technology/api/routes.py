from rest_framework.routers import DefaultRouter
from .views import TechnologiesViewSet

router = DefaultRouter()
router.register(r'technologies', TechnologiesViewSet, basename='technology')

urlpatterns = router.urls
