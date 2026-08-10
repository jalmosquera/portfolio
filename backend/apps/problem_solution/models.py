from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class ProblemSolution(models.Model):
    project = models.OneToOneField(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="problem_solution",
    )
    problem = models.TextField(blank=True)
    solution = models.TextField(blank=True)

    class Meta:
        verbose_name = "Problem Solution"
        verbose_name_plural = "Problem Solutions"

    def __str__(self):
        return self.project.title


class ProblemSolutionContent(TranslatableModel):
    problem_solution = models.OneToOneField(ProblemSolution, on_delete=models.CASCADE, related_name="localized_content")
    translations = TranslatedFields(problem=models.TextField(blank=True), solution=models.TextField(blank=True))
