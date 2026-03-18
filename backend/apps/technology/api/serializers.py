from rest_framework import serializers
from apps.technology.models import Technologies


class TechnologiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technologies
        fields = ["__all__"]
        read_only_fields = ["created_at",]

