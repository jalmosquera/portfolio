from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from ..models import ProblemSolution
from .serializers import ProblemSolutionSerializer


class ProblemSolutionViewSet(viewsets.ModelViewSet):
    queryset = ProblemSolution.objects.all()
    serializer_class = ProblemSolutionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["project"]
