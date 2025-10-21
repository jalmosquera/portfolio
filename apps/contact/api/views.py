"""
API views for the contact app.
Vistas de API para la app contact.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.contact.models import ContactMessage
from .serializers import ContactMessageSerializer, ContactMessageCreateSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all contact messages / Listar todos los mensajes de contacto",
        description="Retrieve a list of all contact messages received. / Obtiene una lista de todos los mensajes de contacto recibidos.",
        tags=["Contact"],
    ),
    retrieve=extend_schema(
        summary="Retrieve a contact message / Obtener un mensaje de contacto",
        description="Get details of a specific contact message by ID. / Obtiene los detalles de un mensaje de contacto específico por ID.",
        tags=["Contact"],
    ),
    create=extend_schema(
        summary="Create a contact message / Crear un mensaje de contacto",
        description="Submit a new contact message (public endpoint). / Envía un nuevo mensaje de contacto (endpoint público).",
        request=ContactMessageCreateSerializer,
        responses={201: ContactMessageSerializer},
        tags=["Contact"],
    ),
    update=extend_schema(
        summary="Update a contact message / Actualizar un mensaje de contacto",
        description="Update all fields of an existing contact message. / Actualiza todos los campos de un mensaje de contacto existente.",
        tags=["Contact"],
    ),
    partial_update=extend_schema(
        summary="Partial update a contact message / Actualizar parcialmente un mensaje de contacto",
        description="Update specific fields of an existing contact message. / Actualiza campos específicos de un mensaje de contacto existente.",
        tags=["Contact"],
    ),
    destroy=extend_schema(
        summary="Delete a contact message / Eliminar un mensaje de contacto",
        description="Delete an existing contact message. / Elimina un mensaje de contacto existente.",
        tags=["Contact"],
    ),
)
class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing ContactMessage instances.
    Provides CRUD operations and status management for contact messages.

    ViewSet para ver y editar instancias de ContactMessage.
    Proporciona operaciones CRUD y gestión de estado para mensajes de contacto.
    """

    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def get_serializer_class(self):
        """Use different serializer for creation."""
        if self.action == 'create':
            return ContactMessageCreateSerializer
        return ContactMessageSerializer

    @extend_schema(
        summary="Mark message as read / Marcar mensaje como leído",
        description="Mark a contact message as read. / Marca un mensaje de contacto como leído.",
        request=None,
        responses={200: ContactMessageSerializer},
        tags=["Contact"],
    )
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """
        Mark message as read.
        Marcar mensaje como leído.
        """
        message = self.get_object()
        message.is_read = True
        message.save()
        serializer = self.get_serializer(message)
        return Response(serializer.data)

    @extend_schema(
        summary="Mark message as replied / Marcar mensaje como respondido",
        description="Mark a contact message as replied. / Marca un mensaje de contacto como respondido.",
        request=None,
        responses={200: ContactMessageSerializer},
        tags=["Contact"],
    )
    @action(detail=True, methods=['post'])
    def mark_replied(self, request, pk=None):
        """
        Mark message as replied.
        Marcar mensaje como respondido.
        """
        message = self.get_object()
        message.is_replied = True
        message.save()
        serializer = self.get_serializer(message)
        return Response(serializer.data)

    @extend_schema(
        summary="Get unread messages / Obtener mensajes no leídos",
        description="Retrieve only contact messages that haven't been read yet. / Obtiene solo los mensajes de contacto que aún no han sido leídos.",
        responses={200: ContactMessageSerializer(many=True)},
        tags=["Contact"],
    )
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """
        Get unread messages.
        Obtener mensajes no leídos.
        """
        unread_messages = self.queryset.filter(is_read=False)
        serializer = self.get_serializer(unread_messages, many=True)
        return Response(serializer.data)
