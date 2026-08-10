import pytest
from rest_framework import status

from apps.analytics.models import SiteVisitCounter


@pytest.mark.django_db
def test_record_visit_creates_single_counter(api_client):
    response = api_client.post("/api/visits/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    counter = SiteVisitCounter.objects.get(pk=1)
    assert counter.total_visits == 1
    assert counter.first_visit_at is not None
    assert counter.last_visit_at is not None


@pytest.mark.django_db
def test_record_visit_increments_existing_counter(api_client):
    api_client.post("/api/visits/")
    response = api_client.post("/api/visits/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert SiteVisitCounter.objects.get(pk=1).total_visits == 2


@pytest.mark.django_db
def test_visit_count_is_not_public(api_client):
    response = api_client.get("/api/visits/")

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
