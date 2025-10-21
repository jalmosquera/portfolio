"""
Serializers for the projects app.
Serializadores para la app projects.
"""

from rest_framework import serializers
from apps.projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Project model with camelCase field names.
    Serializador para el modelo Project con nombres de campos en camelCase.
    """

    shortDescription = serializers.CharField(source='short_description', required=False, allow_blank=True)
    imageUrl = serializers.ImageField(source='image', required=False, allow_null=True)
    githubUrl = serializers.URLField(source='github_url', required=False, allow_blank=True)
    isFeatured = serializers.BooleanField(source='is_featured', default=False)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'shortDescription',
            'imageUrl',
            'url',
            'githubUrl',
            'technologies',
            'isFeatured',
            'order',
            'createdAt',
            'updatedAt',
        ]
        read_only_fields = ['id', 'createdAt', 'updatedAt']
