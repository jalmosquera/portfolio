from rest_framework import viewsets
from ..models import Technologies
from .serializers import TechnologiesSerializer


class TechnologiesViewSet(viewsets.ModelViewSet):
    queryset = Technologies.objects.all()
    serializer_class = TechnologiesSerializer
   # permission_classes = [IsAuthenticated]

