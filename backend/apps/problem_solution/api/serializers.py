from rest_framework import serializer


class ProblemSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemSolution 
        fields = ["__all__"]
        read_only_fields = ["id", "created_at"]

