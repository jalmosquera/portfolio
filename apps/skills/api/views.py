"""
API views for the skills app.
Vistas de API para la app skills.
"""

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.skills.models import Skill, SkillCategory
from .serializers import SkillSerializer, SkillCategorySerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all skills / Listar todas las habilidades",
        description="Retrieve a list of all skills with search and ordering support. / Obtiene una lista de todas las habilidades con soporte de búsqueda y ordenamiento.",
        tags=["Skills"],
    ),
    retrieve=extend_schema(
        summary="Retrieve a skill / Obtener una habilidad",
        description="Get details of a specific skill by ID. / Obtiene los detalles de una habilidad específica por ID.",
        tags=["Skills"],
    ),
    create=extend_schema(
        summary="Create a skill / Crear una habilidad",
        description="Create a new skill. / Crea una nueva habilidad.",
        tags=["Skills"],
    ),
    update=extend_schema(
        summary="Update a skill / Actualizar una habilidad",
        description="Update all fields of an existing skill. / Actualiza todos los campos de una habilidad existente.",
        tags=["Skills"],
    ),
    partial_update=extend_schema(
        summary="Partial update a skill / Actualizar parcialmente una habilidad",
        description="Update specific fields of an existing skill. / Actualiza campos específicos de una habilidad existente.",
        tags=["Skills"],
    ),
    destroy=extend_schema(
        summary="Delete a skill / Eliminar una habilidad",
        description="Delete an existing skill. / Elimina una habilidad existente.",
        tags=["Skills"],
    ),
)
class SkillViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Skill instances.
    Provides CRUD operations and filtering for skills.

    ViewSet para ver y editar instancias de Skill.
    Proporciona operaciones CRUD y filtrado para habilidades.
    """

    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['order', 'name', 'percentage']
    ordering = ['category__order', 'order', 'name']

    @extend_schema(
        summary="Get featured skills / Obtener habilidades destacadas",
        description="Retrieve only skills marked as featured. / Obtiene solo las habilidades marcadas como destacadas.",
        responses={200: SkillSerializer(many=True)},
        tags=["Skills"],
    )
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Get featured skills only.
        Obtener solo habilidades destacadas.
        """
        featured_skills = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(featured_skills, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Get skills grouped by category / Obtener habilidades agrupadas por categoría",
        description="Retrieve all skill categories with their associated skills. / Obtiene todas las categorías de habilidades con sus habilidades asociadas.",
        responses={200: SkillCategorySerializer(many=True)},
        tags=["Skills"],
    )
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """
        Get skills grouped by category.
        Obtener habilidades agrupadas por categoría.
        """
        categories = SkillCategory.objects.all()
        serializer = SkillCategorySerializer(categories, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="List all skill categories / Listar todas las categorías de habilidades",
        description="Retrieve a list of all skill categories with their skills. / Obtiene una lista de todas las categorías de habilidades con sus habilidades.",
        tags=["Skills"],
    ),
    retrieve=extend_schema(
        summary="Retrieve a skill category / Obtener una categoría de habilidades",
        description="Get details of a specific skill category by ID. / Obtiene los detalles de una categoría de habilidades específica por ID.",
        tags=["Skills"],
    ),
    create=extend_schema(
        summary="Create a skill category / Crear una categoría de habilidades",
        description="Create a new skill category. / Crea una nueva categoría de habilidades.",
        tags=["Skills"],
    ),
    update=extend_schema(
        summary="Update a skill category / Actualizar una categoría de habilidades",
        description="Update all fields of an existing skill category. / Actualiza todos los campos de una categoría de habilidades existente.",
        tags=["Skills"],
    ),
    partial_update=extend_schema(
        summary="Partial update a skill category / Actualizar parcialmente una categoría de habilidades",
        description="Update specific fields of an existing skill category. / Actualiza campos específicos de una categoría de habilidades existente.",
        tags=["Skills"],
    ),
    destroy=extend_schema(
        summary="Delete a skill category / Eliminar una categoría de habilidades",
        description="Delete an existing skill category. / Elimina una categoría de habilidades existente.",
        tags=["Skills"],
    ),
)
class SkillCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing SkillCategory instances.
    Provides CRUD operations for skill categories.

    ViewSet para ver y editar instancias de SkillCategory.
    Proporciona operaciones CRUD para categorías de habilidades.
    """

    queryset = SkillCategory.objects.all()
    serializer_class = SkillCategorySerializer
    ordering = ['order', 'name']
