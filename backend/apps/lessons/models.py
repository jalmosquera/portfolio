from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class Lesson(models.Model):
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="lessons",
    )
    text = models.TextField(blank=True)

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"

    def __str__(self):
        return self.text[:50]  


class LessonContent(TranslatableModel):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name="localized_content")
    translations = TranslatedFields(text=models.TextField(blank=True))
