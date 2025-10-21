"""
Projects app URL configuration.
Configuración de URLs para la app projects.
"""

from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [
    path("", views.project_list, name="list"),
    path("<int:pk>/", views.project_detail, name="detail"),
    path("featured/", views.featured_projects, name="featured"),
]
