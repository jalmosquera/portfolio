from rest_framework.routers import DefaultRouter
from .views import ProblemSolutionViewSet

router = DefaultRouter()
router.register(r"problem-solutions", ProblemSolutionViewSet, basename="problem-solution")

urlpatterns = router.urls

