from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from ..models import TechDetail
from .serializers import TechDetailSerializer



class TechDetailViewSet(viewsets.ModelViewSet):
    queryset = TechDetail.objects.all()
    serializer_class = TechDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["project"]
