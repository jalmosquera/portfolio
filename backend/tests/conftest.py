import pytest
import factory
from factory.django import DjangoModelFactory
from rest_framework.test import APIClient

from apps.technology.models import Technologies
from apps.projects.models import Project
from apps.project_images.models import ProjectImage
from apps.tech_details.models import TechDetail
from apps.lessons.models import Lesson
from apps.problem_solution.models import ProblemSolution


class TechnologiesFactory(DjangoModelFactory):
    class Meta:
        model = Technologies

    name = factory.Sequence(lambda n: f"Tech {n}")
    icon = "devicon-python-plain"
    color = "#3776ab"


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    title = factory.Sequence(lambda n: f"Project {n}")
    slug = factory.Sequence(lambda n: f"project-{n}")
    short_description = "Short description of the project."
    description = "Full description of the project."
    github = "https://github.com/example/project"
    live_url = "https://example.com"
    is_featured = False


class ProjectImageFactory(DjangoModelFactory):
    class Meta:
        model = ProjectImage

    project = factory.SubFactory(ProjectFactory)
    title = factory.Sequence(lambda n: f"Screenshot {n}")
    order = factory.Sequence(lambda n: n)


class TechDetailFactory(DjangoModelFactory):
    class Meta:
        model = TechDetail

    project = factory.SubFactory(ProjectFactory)
    category = "Backend"
    text = "Django REST Framework"


class LessonFactory(DjangoModelFactory):
    class Meta:
        model = Lesson

    project = factory.SubFactory(ProjectFactory)
    text = "I learned how to structure a DRF project properly."


class ProblemSolutionFactory(DjangoModelFactory):
    class Meta:
        model = ProblemSolution

    project = factory.SubFactory(ProjectFactory)
    problem = "The restaurants struggled to manage digital menus."
    solution = "We built a SaaS platform with QR menu and online ordering."


@pytest.fixture
def api_client():
    return APIClient()
