"""
API views for the about app.
Vistas de API para la app about.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.about.models import AboutMe
from .serializers import AboutMeSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all about profiles / Listar todos los perfiles about",
        description="Retrieve a list of all about/bio profiles. / Obtiene una lista de todos los perfiles about/bio.",
        tags=["About"],
    ),
    retrieve=extend_schema(
        summary="Retrieve an about profile / Obtener un perfil about",
        description="Get details of a specific about profile by ID. / Obtiene los detalles de un perfil about específico por ID.",
        tags=["About"],
    ),
    create=extend_schema(
        summary="Create an about profile / Crear un perfil about",
        description="Create a new about/bio profile. / Crea un nuevo perfil about/bio.",
        tags=["About"],
    ),
    update=extend_schema(
        summary="Update an about profile / Actualizar un perfil about",
        description="Update all fields of an existing about profile. / Actualiza todos los campos de un perfil about existente.",
        tags=["About"],
    ),
    partial_update=extend_schema(
        summary="Partial update an about profile / Actualizar parcialmente un perfil about",
        description="Update specific fields of an existing about profile. / Actualiza campos específicos de un perfil about existente.",
        tags=["About"],
    ),
    destroy=extend_schema(
        summary="Delete an about profile / Eliminar un perfil about",
        description="Delete an existing about profile. / Elimina un perfil about existente.",
        tags=["About"],
    ),
)
class AboutMeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing AboutMe instances.
    Provides CRUD operations for personal information and bio.

    ViewSet para ver y editar instancias de AboutMe.
    Proporciona operaciones CRUD para información personal y biografía.
    """

    queryset = AboutMe.objects.all()
    serializer_class = AboutMeSerializer

    @extend_schema(
        summary="Get active about profile / Obtener perfil about activo",
        description="Retrieve the currently active about/bio profile. Only one profile should be active at a time. / Obtiene el perfil about/bio actualmente activo. Solo un perfil debe estar activo a la vez.",
        responses={200: AboutMeSerializer},
        tags=["About"],
    )
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Get the active about profile.
        Obtener el perfil activo de about.
        """
        active_profile = self.queryset.filter(is_active=True).first()
        if active_profile:
            serializer = self.get_serializer(active_profile)
            return Response(serializer.data)
        return Response({})
