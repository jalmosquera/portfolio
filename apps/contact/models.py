"""
Contact app models.
Modelos de la app contact.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactMessage(models.Model):
    """
    Model representing a contact form submission.
    Modelo que representa un envío de formulario de contacto.
    """

    name = models.CharField(max_length=200, verbose_name=_("Name"), help_text=_("Sender's name"))
    email = models.EmailField(verbose_name=_("Email"), help_text=_("Sender's email"))
    subject = models.CharField(max_length=300, verbose_name=_("Subject"), help_text=_("Message subject"))
    message = models.TextField(verbose_name=_("Message"), help_text=_("Message content"))
    phone = models.CharField(max_length=20, verbose_name=_("Phone"), help_text=_("Contact phone number"), blank=True)
    is_read = models.BooleanField(default=False, verbose_name=_("Read"), help_text=_("Mark as read"))
    is_replied = models.BooleanField(default=False, verbose_name=_("Replied"), help_text=_("Mark as replied"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Contact Message")
        verbose_name_plural = _("Contact Messages")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"
