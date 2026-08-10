import pytest
from rest_framework import status


def test_api_root_exposes_production_endpoints(api_client):
    response = api_client.get("/api/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "ok",
        "health": "/api/health/",
        "schema": "/api/schema/",
        "documentation": "/api/swagger/",
    }


@pytest.mark.django_db
def test_health_endpoint_checks_database(api_client):
    response = api_client.get("/api/health/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}
