from rest_framework import serializers
from apps.technology.models import Technologies


class TechnologiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technologies
        fields = "__all__"

