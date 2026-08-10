from rest_framework import serializers
from ..models import ProblemSolution
from core.i18n import LocalizedRepresentationMixin


class ProblemSolutionSerializer(LocalizedRepresentationMixin, serializers.ModelSerializer):
    localized_fields = {"problem": "localized_content", "solution": "localized_content"}
    class Meta:
        model = ProblemSolution
        fields = "__all__"
        read_only_fields = ["id"]
