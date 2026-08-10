from rest_framework import serializers

from ..models import Resume


class ResumeSerializer(serializers.ModelSerializer):
    formats = serializers.SerializerMethodField()

    class Meta:
        model = Resume
        fields = ["name", "public_filename", "formats", "updated_at"]

    def get_formats(self, obj):
        return [
            {"id": "concise", "label": "Concise", "includes_portrait": False},
            {"id": "visual", "label": "Visual", "includes_portrait": True},
        ]


class ResumeDownloadQuerySerializer(serializers.Serializer):
    variant = serializers.ChoiceField(choices=["concise", "visual"], default="concise")
