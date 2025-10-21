"""
Global pytest configuration and fixtures for the portfolio project.
"""

import pytest
from django.conf import settings
from django.test import RequestFactory


@pytest.fixture(scope='session')
def django_db_setup():
    """Configure the test database."""
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }


@pytest.fixture
def request_factory():
    """Fixture for Django RequestFactory."""
    return RequestFactory()


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    """Configure media storage for tests."""
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def api_client():
    """Fixture for DRF API client - available across all test modules."""
    from rest_framework.test import APIClient
    return APIClient()
