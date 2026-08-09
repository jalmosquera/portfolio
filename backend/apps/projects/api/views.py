from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Project
from .serializers import SerializerProject


class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = SerializerProject
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_featured', 'slug']
