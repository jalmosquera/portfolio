from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from ..models import About, AboutTranslation


class AboutTranslationSerializer(serializers.Serializer):
    title = serializers.CharField()
    body = serializers.CharField()
    location = serializers.CharField(allow_blank=True)
    availability = serializers.CharField(allow_blank=True)


class AboutSerializer(serializers.ModelSerializer):
    translations = serializers.SerializerMethodField()

    class Meta:
        model = About
        fields = ["id", "translations", "updated_at"]

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_translations(self, obj) -> dict:
        translations = {}
        for translation_object in AboutTranslation.objects.filter(master_id=obj.pk):
            translation = {
                "title": translation_object.title,
                "body": translation_object.body,
                "location": translation_object.location,
                "availability": translation_object.availability,
            }
            translations[translation_object.language_code] = AboutTranslationSerializer(translation).data
        return translations
