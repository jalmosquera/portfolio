from rest_framework import serializers
from ..models import TechDetail
from core.i18n import LocalizedRepresentationMixin


class TechDetailSerializer(LocalizedRepresentationMixin, serializers.ModelSerializer):
    localized_fields = {"category": "localized_content", "text": "localized_content"}
    class Meta:
        model = TechDetail
        fields = "__all__"
