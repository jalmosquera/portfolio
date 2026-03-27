from rest_framework impeor viewset 
from ..models import Lesson

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

