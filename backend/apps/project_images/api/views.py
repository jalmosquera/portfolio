from rest_framework import viewsets
from ..models import ProjectImage
from .serializers import ProjectImageSerializer


class ProjectImageViewSet(viewsets.ModelViewSet):
    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImageSerializer




