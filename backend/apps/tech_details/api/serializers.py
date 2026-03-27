from rest_framework import serializer 
from ..models import TechDetail

class TechDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechDetail
        fields = ["__all__"]

