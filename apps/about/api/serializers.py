"""
Serializers for the about app.
Serializadores para la app about.
"""

from rest_framework import serializers
from apps.about.models import AboutMe


class AboutMeSerializer(serializers.ModelSerializer):
    """
    Serializer for AboutMe model with camelCase field names.
    Serializador para el modelo AboutMe con nombres de campos en camelCase.
    """

    profileImage = serializers.ImageField(source='profile_image', required=False, allow_null=True)
    resumeFile = serializers.FileField(source='resume_file', required=False, allow_null=True)
    linkedinUrl = serializers.URLField(source='linkedin_url', required=False, allow_blank=True)
    githubUrl = serializers.URLField(source='github_url', required=False, allow_blank=True)
    twitterUrl = serializers.URLField(source='twitter_url', required=False, allow_blank=True)
    websiteUrl = serializers.URLField(source='website_url', required=False, allow_blank=True)
    isActive = serializers.BooleanField(source='is_active', default=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = AboutMe
        fields = [
            'id',
            'name',
            'title',
            'bio',
            'email',
            'phone',
            'location',
            'profileImage',
            'resumeFile',
            'linkedinUrl',
            'githubUrl',
            'twitterUrl',
            'websiteUrl',
            'isActive',
            'createdAt',
            'updatedAt',
        ]
        read_only_fields = ['id', 'createdAt', 'updatedAt']
