from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Lesson
from .serializers import LessonSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["project"]
