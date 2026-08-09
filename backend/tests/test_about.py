import pytest
from django.core.management import call_command
from rest_framework import status

from apps.about.models import About


@pytest.mark.django_db
def test_seed_about_creates_bilingual_singleton():
    call_command("seed_about")

    about = About.objects.get()
    assert list(about.get_available_languages()) == ["en", "es"]
    assert about.safe_translation_getter("title", language_code="en") == "About me"
    assert about.safe_translation_getter("title", language_code="es") == "Sobre mí"


@pytest.mark.django_db
def test_seed_about_is_idempotent():
    call_command("seed_about")
    call_command("seed_about")

    assert About.objects.count() == 1


@pytest.mark.django_db
def test_about_api_returns_both_translations(api_client):
    call_command("seed_about")

    response = api_client.get("/api/about/")

    assert response.status_code == status.HTTP_200_OK
    assert set(response.data["translations"]) == {"en", "es"}
    assert "FastAPI" in response.data["translations"]["es"]["body"]
    assert "homelab" in response.data["translations"]["en"]["body"]


@pytest.mark.django_db
def test_about_api_hides_inactive_content(api_client):
    call_command("seed_about")
    About.objects.update(is_visible=False)

    response = api_client.get("/api/about/")

    assert response.status_code == status.HTTP_404_NOT_FOUND
