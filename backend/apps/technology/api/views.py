from rest_framework import viewdet
from ..models import Technologies
from .serializer import TechnologiesSerializer


class TechnologiesViewSet(viewsets.ModelViewSet):
    queryset = Technologies.objects.all()
    serializer_class = TechnologiesSerializer
   # permission_classes = [IsAuthenticated]

