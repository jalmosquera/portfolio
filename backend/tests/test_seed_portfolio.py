import pytest
from django.core.management import call_command

from apps.lessons.models import Lesson
from apps.problem_solution.models import ProblemSolution
from apps.project_images.models import ProjectImage
from apps.projects.models import Project
from apps.tech_details.models import TechDetail
from apps.technology.models import Technologies


@pytest.mark.django_db
def test_seed_portfolio_creates_complete_demo_data(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path

    call_command("seed_portfolio")

    assert Project.objects.count() == 3
    assert Technologies.objects.count() == 7
    assert Project.objects.filter(is_featured=True).count() == 3
    assert ProblemSolution.objects.count() == 3
    assert ProjectImage.objects.count() == 3
    assert TechDetail.objects.count() == 12
    assert Lesson.objects.count() == 6
    assert all(project.image.name.endswith(".svg") for project in Project.objects.all())


@pytest.mark.django_db
def test_seed_portfolio_is_idempotent(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path

    call_command("seed_portfolio")
    call_command("seed_portfolio")

    assert Project.objects.count() == 3
    assert Technologies.objects.count() == 7
    assert ProblemSolution.objects.count() == 3
    assert ProjectImage.objects.count() == 3
    assert TechDetail.objects.count() == 12
    assert Lesson.objects.count() == 6
