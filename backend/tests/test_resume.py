import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework import status

from apps.resume.models import Resume


PDF_CONTENT = b"%PDF-1.4\nportfolio cv\n%%EOF"


@pytest.mark.django_db
class TestResumeApi:
    @override_settings(MEDIA_ROOT="/tmp/portfolio-test-media")
    def test_returns_metadata_and_downloads_pdf(self, api_client):
        resume = Resume.objects.create(
            file=SimpleUploadedFile("cv.pdf", PDF_CONTENT, content_type="application/pdf"),
            public_filename="Jalberth_Mosquera_CV.pdf",
        )

        detail = api_client.get("/api/cv/")
        download = api_client.get("/api/cv/download/")

        assert detail.status_code == status.HTTP_200_OK
        assert detail.data["public_filename"] == "Jalberth_Mosquera_CV.pdf"
        assert download.status_code == status.HTTP_200_OK
        assert download["Content-Type"] == "application/pdf"
        assert "attachment" in download["Content-Disposition"]
        assert b"".join(download.streaming_content) == PDF_CONTENT
        resume.refresh_from_db()
        assert resume.download_count == 1
        resume.file.delete(save=False)

    def test_returns_404_when_resume_is_not_uploaded(self, api_client):
        assert api_client.get("/api/cv/").status_code == status.HTTP_404_NOT_FOUND
        assert api_client.get("/api/cv/download/").status_code == status.HTTP_404_NOT_FOUND

    def test_rejects_a_file_that_is_not_a_pdf(self):
        resume = Resume(
            file=SimpleUploadedFile("cv.pdf", b"not a pdf", content_type="application/pdf")
        )

        with pytest.raises(ValidationError):
            resume.full_clean()
