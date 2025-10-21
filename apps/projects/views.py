"""
Projects app views.
Vistas de la app projects.
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Project


@require_http_methods(["GET"])
def project_list(request):
    """
    Return list of all projects in JSON format with camelCase keys.
    Retorna lista de todos los proyectos en formato JSON con llaves en camelCase.
    """
    projects = Project.objects.all()

    data = {
        "success": True,
        "projects": [project.to_dict() for project in projects]
    }

    return JsonResponse(data)


@require_http_methods(["GET"])
def project_detail(request, pk):
    """
    Return single project details in JSON format with camelCase keys.
    Retorna detalles de un proyecto en formato JSON con llaves en camelCase.
    """
    try:
        project = Project.objects.get(pk=pk)
        data = {
            "success": True,
            "project": project.to_dict()
        }
        return JsonResponse(data)
    except Project.DoesNotExist:
        return JsonResponse({
            "success": False,
            "error": "Project not found"
        }, status=404)


@require_http_methods(["GET"])
def featured_projects(request):
    """
    Return featured projects in JSON format with camelCase keys.
    Retorna proyectos destacados en formato JSON con llaves en camelCase.
    """
    projects = Project.objects.filter(is_featured=True)

    data = {
        "success": True,
        "projects": [project.to_dict() for project in projects]
    }

    return JsonResponse(data)
