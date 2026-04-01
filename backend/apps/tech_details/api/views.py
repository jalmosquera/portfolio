from rest_framework import viewsets
from ..models import TechDetail
from .serializers import TechDetailSerializer



class TechDetailViewSet(viewsets.ModelViewSet):
    queryset = TechDetail.objects.all()
    serializer_class = TechDetailSerializer

