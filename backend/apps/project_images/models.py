from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from core.images import optimize_raster_image


class ProjectImage(models.Model):
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="gallery",
    )
    image = models.ImageField(upload_to="project_images/", null=True, blank=True)
    title = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"
        ordering = ["order"]

    def __str__(self):
        return f"{self.project.title} - {self.title or 'Image'}"

    def save(self, *args, **kwargs):
        if self.image and not self.image._committed:
            optimized = optimize_raster_image(self.image)
            if optimized:
                self.image = optimized
        super().save(*args, **kwargs)


class ProjectImageContent(TranslatableModel):
    project_image = models.OneToOneField(ProjectImage, on_delete=models.CASCADE, related_name="localized_content")
    translations = TranslatedFields(title=models.CharField(max_length=255, blank=True))
