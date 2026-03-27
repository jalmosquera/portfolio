from rest_framework import viewset
from ..models import TechDetail
from .serializer import TechDetailSerializer



class TechDetailViewSet(viewsets.ModelViewSet):
    queryset = TechDetail.objects.all()
    serializer_class = TechDetailSerializer

