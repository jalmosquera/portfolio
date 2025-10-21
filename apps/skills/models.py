"""
Skills app models.
Modelos de la app skills.
"""

from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _


class SkillCategory(models.Model):
    """
    Model representing a skill category.
    Modelo que representa una categoría de habilidades.
    """

    name = models.CharField(max_length=100, verbose_name=_("Category Name"), help_text=_("Name of the skill category"))
    description = models.TextField(verbose_name=_("Description"), help_text=_("Category description"), blank=True)
    order = models.IntegerField(default=0, verbose_name=_("Order"), help_text=_("Display order (lower numbers first)"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Skill Category")
        verbose_name_plural = _("Skill Categories")
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Skill(models.Model):
    """
    Model representing a skill or technology.
    Modelo que representa una habilidad o tecnología.
    """

    PROFICIENCY_CHOICES = [
        ('beginner', _('Beginner')),
        ('intermediate', _('Intermediate')),
        ('advanced', _('Advanced')),
        ('expert', _('Expert')),
    ]

    name = models.CharField(max_length=100, verbose_name=_("Skill Name"), help_text=_("Name of the skill or technology"))
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills', verbose_name=_("Category"), help_text=_("Skill category"))
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES, default='intermediate', verbose_name=_("Proficiency Level"), help_text=_("Level of proficiency"))
    percentage = models.IntegerField(default=50, verbose_name=_("Percentage"), help_text=_("Proficiency percentage (0-100)"), validators=[validators.MinValueValidator(0), validators.MaxValueValidator(100)])
    icon = models.CharField(max_length=100, verbose_name=_("Icon"), help_text=_("Icon class or URL"), blank=True)
    description = models.TextField(verbose_name=_("Description"), help_text=_("Skill description"), blank=True)
    years_experience = models.IntegerField(default=0, verbose_name=_("Years of Experience"), help_text=_("Years of experience with this skill"), validators=[validators.MinValueValidator(0)])
    is_featured = models.BooleanField(default=False, verbose_name=_("Featured"), help_text=_("Display in featured skills"))
    order = models.IntegerField(default=0, verbose_name=_("Order"), help_text=_("Display order within category"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")
        ordering = ["category__order", "order", "name"]

    def __str__(self):
        return f"{self.name} ({self.category.name})"
