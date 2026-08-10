from rest_framework import serializers
from ..models import Project
from apps.technology.api.serializers import TechnologiesSerializer
from core.i18n import LocalizedRepresentationMixin


class SerializerProject(LocalizedRepresentationMixin, serializers.ModelSerializer):
    localized_fields = {"title": "localized_content", "short_description": "localized_content", "description": "localized_content"}
    technologies = TechnologiesSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ["created_at"]
