from django.db import models


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
