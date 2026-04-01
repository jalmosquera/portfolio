from rest_framework import serializers
from ..models import TechDetail


class TechDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechDetail
        fields = "__all__"
