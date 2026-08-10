from unittest.mock import patch

import pytest
from django.core import mail
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APIClient

from apps.contact.models import ContactInquiry


VALID_PAYLOAD = {
    "company_or_recruiter": "Acme Recruiting",
    "phone": "+34 600 123 456",
    "email": "recruiter@example.com",
    "description": "We would like to discuss a backend engineering opportunity.",
}


@pytest.fixture(autouse=True)
def clear_throttle_cache():
    cache.clear()


@pytest.mark.django_db
def test_contact_api_creates_inquiry(api_client):
    response = api_client.post("/api/contact/", VALID_PAYLOAD, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert ContactInquiry.objects.count() == 1
    assert response.data["status"] == ContactInquiry.Status.NEW


@pytest.mark.django_db
def test_contact_api_does_not_require_csrf_for_admin_session():
    user = get_user_model().objects.create_user(
        username="portfolio-admin",
        password="test-password",
    )
    client = APIClient(enforce_csrf_checks=True)
    client.force_login(user)

    response = client.post("/api/contact/", VALID_PAYLOAD, format="json")

    assert response.status_code == status.HTTP_201_CREATED


@override_settings(
    EMAIL_NOTIFICATIONS_ENABLED=True,
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="Jalberth Mosquera <jmosquera2305@gmail.com>",
    CONTACT_NOTIFICATION_EMAIL="jmosquera2305@gmail.com",
)
@pytest.mark.django_db
def test_contact_api_sends_notification_and_spanish_confirmation(api_client):
    response = api_client.post(
        "/api/contact/",
        VALID_PAYLOAD,
        format="json",
        HTTP_ACCEPT_LANGUAGE="es",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert len(mail.outbox) == 2
    assert mail.outbox[0].to == ["jmosquera2305@gmail.com"]
    assert mail.outbox[0].reply_to == [VALID_PAYLOAD["email"]]
    assert mail.outbox[1].to == [VALID_PAYLOAD["email"]]
    assert mail.outbox[1].subject == "Recibí tu mensaje"
    assert "Tenés una nueva consulta" in mail.outbox[0].alternatives[0].content
    inquiry = ContactInquiry.objects.get()
    assert inquiry.notification_sent_at is not None
    assert inquiry.confirmation_sent_at is not None
    assert inquiry.email_error == ""


@override_settings(EMAIL_NOTIFICATIONS_ENABLED=True)
@pytest.mark.django_db
def test_contact_api_keeps_inquiry_when_smtp_fails(api_client):
    with patch(
        "apps.contact.services.email_notifications.EmailMultiAlternatives.send",
        side_effect=OSError("SMTP unavailable"),
    ):
        response = api_client.post("/api/contact/", VALID_PAYLOAD, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    inquiry = ContactInquiry.objects.get()
    assert inquiry.notification_sent_at is None
    assert inquiry.confirmation_sent_at is None
    assert "SMTP unavailable" in inquiry.email_error


@pytest.mark.django_db
@pytest.mark.parametrize("field", ["company_or_recruiter", "phone", "email", "description"])
def test_contact_api_requires_all_public_fields(api_client, field):
    payload = {key: value for key, value in VALID_PAYLOAD.items() if key != field}

    response = api_client.post("/api/contact/", payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert field in response.data


@pytest.mark.django_db
def test_contact_api_validates_email(api_client):
    response = api_client.post(
        "/api/contact/",
        {**VALID_PAYLOAD, "email": "not-an-email"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data


@pytest.mark.django_db
def test_contact_api_validates_phone(api_client):
    response = api_client.post(
        "/api/contact/",
        {**VALID_PAYLOAD, "phone": "abc"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "phone" in response.data


@pytest.mark.django_db
def test_contact_api_rejects_short_description(api_client):
    response = api_client.post(
        "/api/contact/",
        {**VALID_PAYLOAD, "description": "Too short"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "description" in response.data


@pytest.mark.django_db
def test_contact_api_throttles_repeated_submissions(api_client):
    for _ in range(5):
        response = api_client.post("/api/contact/", VALID_PAYLOAD, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    response = api_client.post("/api/contact/", VALID_PAYLOAD, format="json")

    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
