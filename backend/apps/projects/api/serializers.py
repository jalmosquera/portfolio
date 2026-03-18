from rest_framework import serializers 

class SerializerProject(serializers.ModelSerializer):
    class Meta:
        model = 
        fields = ["__all__"]
        read_only_fields = ["created_at"]
)
