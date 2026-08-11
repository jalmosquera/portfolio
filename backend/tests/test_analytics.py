import pytest
from datetime import timedelta

from django.contrib.auth import get_user_model
from rest_framework import status

from apps.analytics.models import DailySiteVisit, SiteVisitCounter, analytics_today


@pytest.mark.django_db
def test_record_visit_creates_single_counter(api_client):
    response = api_client.post("/api/visits/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    counter = SiteVisitCounter.objects.get(pk=1)
    assert counter.total_visits == 1
    assert counter.first_visit_at is not None
    assert counter.last_visit_at is not None
    assert DailySiteVisit.objects.get(date=analytics_today()).visits == 1


@pytest.mark.django_db
def test_record_visit_increments_existing_counter(api_client):
    api_client.post("/api/visits/")
    response = api_client.post("/api/visits/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert SiteVisitCounter.objects.get(pk=1).total_visits == 2
    assert DailySiteVisit.objects.get(date=analytics_today()).visits == 2


@pytest.mark.django_db
def test_visit_count_is_not_public(api_client):
    response = api_client.get("/api/visits/")

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_analytics_summary_requires_authentication(api_client):
    response = api_client.get("/api/analytics/summary/")

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_analytics_summary_rejects_staff_non_superuser(api_client):
    user = get_user_model().objects.create_user(username="staff", password="safe-password", is_staff=True)
    api_client.force_login(user)

    response = api_client.get("/api/analytics/summary/")

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_analytics_summary_returns_daily_weekly_and_monthly_data_for_superuser(api_client):
    today = analytics_today()
    yesterday = today - timedelta(days=1)
    DailySiteVisit.objects.create(date=yesterday, visits=3)
    DailySiteVisit.objects.create(date=today, visits=5)
    SiteVisitCounter.objects.create(pk=1, total_visits=21)
    user = get_user_model().objects.create_superuser(
        username="owner",
        email="owner@example.com",
        password="safe-password",
    )
    api_client.force_login(user)

    response = api_client.get("/api/analytics/summary/")

    assert response.status_code == status.HTTP_200_OK
    assert response["Cache-Control"] == "private, no-store"
    assert response.data["today"] == 5
    assert response.data["current_week"] >= 5
    assert response.data["current_month"] >= 5
    assert response.data["all_time"] == 21
    assert len(response.data["daily"]) == 30
    assert len(response.data["weekly"]) == 12
    assert len(response.data["monthly"]) == 12
    assert response.data["daily"][-1] == {"label": today.isoformat(), "visits": 5}
