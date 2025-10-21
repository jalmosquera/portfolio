"""
Projects app models.
Modelos de la app projects.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    """
    Model representing a portfolio project.
    Modelo que representa un proyecto del portfolio.
    """

    title = models.CharField(max_length=200, verbose_name=_("Title"), help_text=_("Project title"))
    description = models.TextField(verbose_name=_("Description"), help_text=_("Detailed project description"))
    short_description = models.CharField(max_length=300, verbose_name=_("Short Description"), help_text=_("Brief project summary"), blank=True)
    image = models.ImageField(upload_to="projects/", verbose_name=_("Image"), help_text=_("Project image or screenshot"), blank=True, null=True)
    url = models.URLField(verbose_name=_("Project URL"), help_text=_("Live project URL"), blank=True)
    github_url = models.URLField(verbose_name=_("GitHub URL"), help_text=_("GitHub repository URL"), blank=True)
    technologies = models.CharField(max_length=500, verbose_name=_("Technologies"), help_text=_("Technologies used (comma-separated)"), blank=True)
    is_featured = models.BooleanField(default=False, verbose_name=_("Featured"), help_text=_("Display in featured section"))
    order = models.IntegerField(default=0, verbose_name=_("Order"), help_text=_("Display order (lower numbers first)"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    def to_dict(self):
        """
        Convert model to dictionary with camelCase keys.
        Convertir modelo a diccionario con llaves en camelCase.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "shortDescription": self.short_description,
            "imageUrl": self.image.url if self.image else None,
            "url": self.url,
            "githubUrl": self.github_url,
            "technologies": self.technologies.split(",") if self.technologies else [],
            "isFeatured": self.is_featured,
            "order": self.order,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
        }
