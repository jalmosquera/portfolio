from rest_framework import serializers
from ..models import Lesson
from core.i18n import LocalizedRepresentationMixin


class LessonSerializer(LocalizedRepresentationMixin, serializers.ModelSerializer):
    localized_fields = {"text": "localized_content"}
    class Meta:
        model = Lesson
        fields = "__all__"
        read_only_fields = ["id"]
