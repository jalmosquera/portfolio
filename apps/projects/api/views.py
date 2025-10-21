"""
API views for the projects app.
Vistas de API para la app projects.
"""

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from apps.projects.models import Project
from .serializers import ProjectSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all projects / Listar todos los proyectos",
        description="Retrieve a list of all portfolio projects with pagination, search and ordering support. / Obtiene una lista de todos los proyectos del portfolio con soporte de paginación, búsqueda y ordenamiento.",
        tags=["Projects"],
    ),
    retrieve=extend_schema(
        summary="Retrieve a project / Obtener un proyecto",
        description="Get details of a specific project by ID. / Obtiene los detalles de un proyecto específico por ID.",
        tags=["Projects"],
    ),
    create=extend_schema(
        summary="Create a project / Crear un proyecto",
        description="Create a new portfolio project. / Crea un nuevo proyecto de portfolio.",
        tags=["Projects"],
    ),
    update=extend_schema(
        summary="Update a project / Actualizar un proyecto",
        description="Update all fields of an existing project. / Actualiza todos los campos de un proyecto existente.",
        tags=["Projects"],
    ),
    partial_update=extend_schema(
        summary="Partial update a project / Actualizar parcialmente un proyecto",
        description="Update specific fields of an existing project. / Actualiza campos específicos de un proyecto existente.",
        tags=["Projects"],
    ),
    destroy=extend_schema(
        summary="Delete a project / Eliminar un proyecto",
        description="Delete an existing project. / Elimina un proyecto existente.",
        tags=["Projects"],
    ),
)
class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Project instances.
    Provides CRUD operations and filtering for portfolio projects.

    ViewSet para ver y editar instancias de Project.
    Proporciona operaciones CRUD y filtrado para proyectos de portfolio.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['title', 'description', 'technologies']
    ordering_fields = ['order', 'created_at', 'title']
    ordering = ['order', '-created_at']

    @extend_schema(
        summary="Get featured projects / Obtener proyectos destacados",
        description="Retrieve only projects marked as featured. / Obtiene solo los proyectos marcados como destacados.",
        responses={200: ProjectSerializer(many=True)},
        tags=["Projects"],
    )
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Get featured projects only.
        Obtener solo proyectos destacados.
        """
        featured_projects = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(featured_projects, many=True)
        return Response(serializer.data)
