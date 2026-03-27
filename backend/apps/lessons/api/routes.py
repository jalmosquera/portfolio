from rest_framework.routers import DefaultRouter
from .views import Lesson

router = DefaultRouter()
router.register(r"lesson", Lesson, basename="lesson")

urlpatterns = router.urls

