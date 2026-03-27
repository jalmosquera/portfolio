from rest_framework import viewset
from ..models import ProjectImage
from .serializer import ProjectImageSerializer 


class ProjectImageViewSet(viewsets.ModelViewSet):
    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImageSerializer




