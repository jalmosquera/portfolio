from rest_framework import serializers
from ..models import ProjectImage
from core.i18n import LocalizedRepresentationMixin


class ProjectImageSerializer(LocalizedRepresentationMixin, serializers.ModelSerializer):
    localized_fields = {"title": "localized_content"}
    class Meta:
        model = ProjectImage
        fields = "__all__"
