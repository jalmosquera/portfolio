from django.core.validators import RegexValidator
from django.db import models


phone_validator = RegexValidator(
    regex=r"^\+?[0-9\s().-]{7,32}$",
    message="Enter a valid phone number.",
)


class ContactInquiry(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        ARCHIVED = "archived", "Archived"

    company_or_recruiter = models.CharField(max_length=160)
    phone = models.CharField(max_length=32, validators=[phone_validator])
    email = models.EmailField()
    description = models.TextField()
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.NEW)
    notification_sent_at = models.DateTimeField(null=True, blank=True)
    confirmation_sent_at = models.DateTimeField(null=True, blank=True)
    email_error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact inquiry"
        verbose_name_plural = "Contact inquiries"

    def __str__(self):
        return f"{self.company_or_recruiter} — {self.email}"
