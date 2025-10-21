"""
About app models.
Modelos de la app about.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class AboutMe(models.Model):
    """
    Model representing personal information for the about section.
    Modelo que representa información personal para la sección sobre mí.
    """

    name = models.CharField(max_length=200, verbose_name=_("Name"), help_text=_("Full name"))
    title = models.CharField(max_length=200, verbose_name=_("Professional Title"), help_text=_("Professional title or role"))
    bio = models.TextField(verbose_name=_("Biography"), help_text=_("Short biography"))
    email = models.EmailField(verbose_name=_("Email"), help_text=_("Contact email"))
    phone = models.CharField(max_length=20, verbose_name=_("Phone"), help_text=_("Contact phone number"), blank=True)
    location = models.CharField(max_length=200, verbose_name=_("Location"), help_text=_("City, Country"), blank=True)
    profile_image = models.ImageField(upload_to="about/", verbose_name=_("Profile Image"), help_text=_("Profile photo"), blank=True, null=True)
    resume_file = models.FileField(upload_to="about/resumes/", verbose_name=_("Resume/CV"), help_text=_("Resume or CV file"), blank=True, null=True)
    linkedin_url = models.URLField(verbose_name=_("LinkedIn URL"), blank=True)
    github_url = models.URLField(verbose_name=_("GitHub URL"), blank=True)
    twitter_url = models.URLField(verbose_name=_("Twitter URL"), blank=True)
    website_url = models.URLField(verbose_name=_("Website URL"), blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_("Active"), help_text=_("Only one profile should be active at a time"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("About Me")
        verbose_name_plural = _("About Me")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Ensure only one active profile exists."""
        if self.is_active:
            AboutMe.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
