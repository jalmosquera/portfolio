"""
Serializers for the skills app.
Serializadores para la app skills.
"""

from rest_framework import serializers
from apps.skills.models import Skill, SkillCategory


class SkillSerializer(serializers.ModelSerializer):
    """
    Serializer for Skill model with camelCase field names.
    Serializador para el modelo Skill con nombres de campos en camelCase.
    """

    categoryId = serializers.PrimaryKeyRelatedField(
        source='category',
        queryset=SkillCategory.objects.all()
    )
    categoryName = serializers.CharField(source='category.name', read_only=True)
    yearsExperience = serializers.IntegerField(source='years_experience')
    isFeatured = serializers.BooleanField(source='is_featured', default=False)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = Skill
        fields = [
            'id',
            'name',
            'categoryId',
            'categoryName',
            'proficiency',
            'percentage',
            'icon',
            'description',
            'yearsExperience',
            'isFeatured',
            'order',
            'createdAt',
            'updatedAt',
        ]
        read_only_fields = ['id', 'categoryName', 'createdAt', 'updatedAt']


class SkillCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for SkillCategory model with camelCase field names.
    Serializador para el modelo SkillCategory con nombres de campos en camelCase.
    """

    skills = SkillSerializer(many=True, read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = SkillCategory
        fields = [
            'id',
            'name',
            'description',
            'order',
            'skills',
            'createdAt',
            'updatedAt',
        ]
        read_only_fields = ['id', 'createdAt', 'updatedAt']
