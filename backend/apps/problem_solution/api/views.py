from rest_framework import viewsets
from ..models import ProblemSolution
from .serializers import ProblemSolutionSerializer


class ProblemSolutionViewSet(viewsets.ModelViewSet):
    queryset = ProblemSolution.objects.all()
    serializer_class = ProblemSolutionSerializer
