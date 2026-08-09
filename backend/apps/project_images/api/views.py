from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from ..models import ProjectImage
from .serializers import ProjectImageSerializer


class ProjectImageViewSet(viewsets.ModelViewSet):
    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["project"]
