"""
Serializers for the contact app.
Serializadores para la app contact.
"""

from rest_framework import serializers
from apps.contact.models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    """
    Serializer for ContactMessage model with camelCase field names.
    Serializador para el modelo ContactMessage con nombres de campos en camelCase.
    """

    isRead = serializers.BooleanField(source='is_read', default=False)
    isReplied = serializers.BooleanField(source='is_replied', default=False)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = ContactMessage
        fields = [
            'id',
            'name',
            'email',
            'subject',
            'message',
            'phone',
            'isRead',
            'isReplied',
            'createdAt',
            'updatedAt',
        ]
        read_only_fields = ['id', 'createdAt', 'updatedAt']


class ContactMessageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating contact messages (public endpoint).
    Serializador para crear mensajes de contacto (endpoint público).
    """

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message', 'phone']
