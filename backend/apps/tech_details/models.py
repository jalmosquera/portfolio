from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class TechDetail(models.Model):
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="tech_details",
    )

    category = models.CharField(max_length=100)
    text = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Tech Detail"
        verbose_name_plural = "Tech Details"

    def __str__(self):
        return f"{self.category}: {self.text}"


class TechDetailContent(TranslatableModel):
    tech_detail = models.OneToOneField(TechDetail, on_delete=models.CASCADE, related_name="localized_content")
    translations = TranslatedFields(
        category=models.CharField(max_length=100),
        text=models.CharField(max_length=255),
    )
