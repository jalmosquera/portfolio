import pytest
from django.core.exceptions import ImproperlyConfigured

from core import settings as project_settings


def test_env_or_file_reads_secret_file(monkeypatch, tmp_path):
    secret_file = tmp_path / "secret"
    secret_file.write_text("generated-secret\n")
    monkeypatch.delenv("TEST_SECRET", raising=False)
    monkeypatch.setenv("TEST_SECRET_FILE", str(secret_file))

    assert project_settings.env_or_file("TEST_SECRET") == "generated-secret"


def test_env_or_file_rejects_ambiguous_configuration(monkeypatch, tmp_path):
    secret_file = tmp_path / "secret"
    secret_file.write_text("file-secret")
    monkeypatch.setenv("TEST_SECRET", "environment-secret")
    monkeypatch.setenv("TEST_SECRET_FILE", str(secret_file))

    with pytest.raises(ImproperlyConfigured, match="either TEST_SECRET or TEST_SECRET_FILE"):
        project_settings.env_or_file("TEST_SECRET")
