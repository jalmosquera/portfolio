from rest_framework import viewsets
from ..models import Project
from .serializers import SerializerProject


class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = SerializerProject
