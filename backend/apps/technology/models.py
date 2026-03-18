from django.db import models


class Technologies(models.Model):
    name = models.CharField(max_length=255, blank=True)
    icon = models.CharField(max_length=255, blank=True)
    color = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Technology"
        verbose_name_plural = "Technologies"

    def __str__(self):
        return self.name

