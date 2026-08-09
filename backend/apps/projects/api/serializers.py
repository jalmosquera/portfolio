from rest_framework import serializers
from ..models import Project
from apps.technology.api.serializers import TechnologiesSerializer


class SerializerProject(serializers.ModelSerializer):
    technologies = TechnologiesSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ["created_at"]
