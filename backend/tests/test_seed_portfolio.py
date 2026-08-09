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
    assert Technologies.objects.count() == 17
    assert Project.objects.filter(is_featured=True).count() == 3
    assert ProblemSolution.objects.count() == 3
    assert ProjectImage.objects.count() == 3
    assert TechDetail.objects.count() == 18
    assert Lesson.objects.count() == 6
    assert all(project.image.name.endswith(".svg") for project in Project.objects.all())


@pytest.mark.django_db
def test_seed_portfolio_is_idempotent(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path

    call_command("seed_portfolio")
    call_command("seed_portfolio")

    assert Project.objects.count() == 3
    assert Technologies.objects.count() == 17
    assert ProblemSolution.objects.count() == 3
    assert ProjectImage.objects.count() == 3
    assert TechDetail.objects.count() == 18
    assert Lesson.objects.count() == 6


@pytest.mark.django_db
def test_seed_portfolio_replaces_legacy_demo_projects(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    legacy_technology = Technologies.objects.create(name="Raspberry Pi")
    legacy_project = Project.objects.create(title="Alternativa Kiosk", slug="alternativa-kiosk")
    legacy_project.technologies.add(legacy_technology)

    call_command("seed_portfolio")

    assert not Project.objects.filter(slug="alternativa-kiosk").exists()
    assert not Technologies.objects.filter(name="Raspberry Pi").exists()
    assert set(Project.objects.values_list("slug", flat=True)) == {
        "alternativa-2-0",
        "eduardo-bernal-abogado",
        "equus-pub-digital-menu",
    }
