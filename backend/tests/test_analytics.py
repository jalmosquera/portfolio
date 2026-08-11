import pytest
from datetime import timedelta
from uuid import uuid4

from django.contrib.auth import get_user_model
from rest_framework import status

from django.utils import timezone

from apps.analytics.models import AnalyticsEvent, AnalyticsSession, DailySiteVisit, SiteVisitCounter, analytics_today


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
    assert response.data["daily"][-1] == {"label": today.isoformat(), "visits": 5, "unique_visitors": 0}


@pytest.mark.django_db
def test_anonymous_session_is_created_and_reused_without_ip(api_client):
    visitor_id = uuid4()
    payload = {
        "visitor_id": str(visitor_id),
        "landing_path": "/?utm_source=linkedin&utm_medium=social&utm_campaign=portfolio",
        "referrer": "https://www.linkedin.com/feed/",
        "utm_source": "linkedin",
        "utm_medium": "social",
        "utm_campaign": "portfolio",
        "device_type": "desktop",
        "browser": "Firefox",
        "operating_system": "Linux",
        "language": "es-ES",
    }
    created = api_client.post("/api/analytics/sessions/", payload, format="json", HTTP_CF_IPCOUNTRY="ES")
    payload["session_id"] = created.data["session_id"]
    reused = api_client.post("/api/analytics/sessions/", payload, format="json")

    assert created.status_code == status.HTTP_201_CREATED
    assert reused.status_code == status.HTTP_200_OK
    assert reused.data["created"] is False
    assert AnalyticsSession.objects.count() == 1
    session = AnalyticsSession.objects.get()
    assert session.source == "LinkedIn"
    assert session.country == "ES"
    assert not any(field.name in {"ip", "ip_address"} for field in AnalyticsSession._meta.fields)


@pytest.mark.django_db
def test_expired_session_creates_returning_session(api_client):
    visitor_id = uuid4()
    old = AnalyticsSession.objects.create(
        visitor_id=visitor_id,
        last_seen_at=timezone.now() - timedelta(minutes=31),
    )

    response = api_client.post(
        "/api/analytics/sessions/",
        {"visitor_id": str(visitor_id), "session_id": str(old.id), "landing_path": "/projects"},
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert AnalyticsSession.objects.count() == 2
    assert AnalyticsSession.objects.exclude(pk=old.pk).get().is_returning is True


@pytest.mark.django_db
def test_event_registration_validates_type_and_updates_session(api_client):
    session = AnalyticsSession.objects.create(visitor_id=uuid4())
    previous_seen = session.last_seen_at
    response = api_client.post(
        "/api/analytics/events/",
        {"session_id": str(session.id), "event_type": "project_view", "path": "/projects/demo", "target": "demo"},
        format="json",
    )
    invalid = api_client.post(
        "/api/analytics/events/",
        {"session_id": str(session.id), "event_type": "made_up"},
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert invalid.status_code == status.HTTP_400_BAD_REQUEST
    assert AnalyticsEvent.objects.get().target == "demo"
    session.refresh_from_db()
    assert session.last_seen_at >= previous_seen


@pytest.mark.django_db
def test_summary_aggregates_unique_visitors_pages_sources_and_projects(api_client):
    visitor = uuid4()
    first = AnalyticsSession.objects.create(visitor_id=visitor, source="Google", device_type="mobile", browser="Chrome", operating_system="Android", country="ES")
    second = AnalyticsSession.objects.create(visitor_id=visitor, source="Direct", is_returning=True, device_type="desktop", browser="Firefox", operating_system="Linux")
    third = AnalyticsSession.objects.create(visitor_id=uuid4(), source="GitHub", device_type="desktop", browser="Safari", operating_system="macOS")
    for session, path in [(first, "/"), (first, "/projects"), (second, "/"), (third, "/")]:
        AnalyticsEvent.objects.create(session=session, event_type="page_view", path=path)
    AnalyticsEvent.objects.create(session=first, event_type="project_view", path="/projects/demo", target="demo")
    AnalyticsEvent.objects.create(session=first, event_type="cv_download", target="es:visual")
    owner = get_user_model().objects.create_superuser(username="analytics-owner", email="owner@example.com", password="safe-password")
    api_client.force_login(owner)

    response = api_client.get("/api/analytics/summary/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["unique_visitors"] == 2
    assert response.data["sessions"] == 3
    assert response.data["pageviews"] == 4
    assert response.data["pages_per_session"] == pytest.approx(1.33)
    assert response.data["new_visitors"] == 2
    assert response.data["returning_visitors"] == 1
    assert response.data["top_pages"][0] == {"label": "/", "value": 3}
    assert response.data["top_projects"][0] == {"label": "demo", "value": 1}
    assert response.data["conversions"]["cv_download"] == 1
    assert {item["label"] for item in response.data["sources"]} == {"Direct", "GitHub", "Google"}
