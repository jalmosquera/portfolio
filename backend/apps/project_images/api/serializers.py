from rest_framework import serializer   
from ..models import ProjectImage   

class  ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ["__all__"]

