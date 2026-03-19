from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="projects", null=True, blank=True)
    github = models.URLField(max_length=200, blank=True)
    live_url = models.URLField(max_length=200, blank=True)
    is_featured = models.BooleanField(default=False)

    technologies = models.ManyToManyField(
        "technology.Technology",
        related_name="projects",
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
