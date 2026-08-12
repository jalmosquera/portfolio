import pytest
from django.core.management import call_command
from rest_framework import status

from apps.resume.models import Resume, ResumeExperience, ResumeSkill


@pytest.fixture(autouse=True)
def resume_data(db, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    call_command("seed_resume", verbosity=0)


@pytest.mark.django_db
class TestResumeApi:
    def test_returns_dynamic_metadata(self, api_client):
        detail = api_client.get("/api/cv/")

        assert detail.status_code == status.HTTP_200_OK
        assert detail.data["name"] == "Jalberth Mosquera"
        assert [item["id"] for item in detail.data["formats"]] == ["concise", "visual"]
        assert Resume.objects.get(singleton=True).portfolio_url == "https://portfolio.mosquerasoft.com/"

    @pytest.mark.parametrize("variant", ["concise", "visual"])
    def test_generates_each_pdf_format_from_database(self, api_client, variant):
        resume = Resume.objects.get(singleton=True)
        resume.content.set_current_language("es")
        resume.content.profile = "Perfil actualizado desde la base de datos."
        resume.content.save()

        response = api_client.get(
            f"/api/cv/download/?variant={variant}",
            HTTP_ACCEPT_LANGUAGE="es",
        )
        content = b"".join(response.streaming_content)

        assert response.status_code == status.HTTP_200_OK
        assert response["Content-Type"] == "application/pdf"
        assert f"_{variant}.pdf" in response["Content-Disposition"]
        assert content.startswith(b"%PDF-")
        assert len(content) > 5_000
        resume.refresh_from_db()
        assert resume.download_count == 1

    def test_rejects_unknown_format(self, api_client):
        response = api_client.get("/api/cv/download/?variant=unknown")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_404_without_active_resume(self, api_client):
        Resume.objects.update(is_active=False)
        assert api_client.get("/api/cv/").status_code == status.HTTP_404_NOT_FOUND
        assert api_client.get("/api/cv/download/").status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_seed_resume_is_idempotent(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    call_command("seed_resume")
    call_command("seed_resume")

    assert Resume.objects.count() == 1
    assert ResumeSkill.objects.count() == 12
    assert ResumeExperience.objects.count() == 1
    assert Resume.objects.get().portrait.name.endswith("jalberth-mosquera.jpg")
