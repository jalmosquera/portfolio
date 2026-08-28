from unittest.mock import patch

import pytest
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
    CONTACT_EMAIL_ASYNC=False,
    RESEND_API_KEY="re_test",
    RESEND_FROM_EMAIL="Portfolio <noreply@mosquerasoft.com>",
    CONTACT_NOTIFICATION_EMAIL="jmosquera2305@gmail.com",
)
@pytest.mark.django_db
def test_contact_api_sends_notification_and_spanish_confirmation(api_client):
    with patch("apps.contact.services.email_notifications.resend.Emails.send") as send_email:
        response = api_client.post(
            "/api/contact/",
            VALID_PAYLOAD,
            format="json",
            HTTP_ACCEPT_LANGUAGE="es",
        )

    assert response.status_code == status.HTTP_201_CREATED
    assert send_email.call_count == 2
    notification, confirmation = [call.args[0] for call in send_email.call_args_list]
    assert notification["to"] == ["jmosquera2305@gmail.com"]
    assert notification["reply_to"] == [VALID_PAYLOAD["email"]]
    assert confirmation["to"] == [VALID_PAYLOAD["email"]]
    assert confirmation["subject"] == "Recibí tu mensaje"
    assert "Tenés una nueva consulta" in notification["html"]
    inquiry = ContactInquiry.objects.get()
    assert inquiry.notification_sent_at is not None
    assert inquiry.confirmation_sent_at is not None
    assert inquiry.email_error == ""


@override_settings(EMAIL_NOTIFICATIONS_ENABLED=True, CONTACT_EMAIL_ASYNC=False, RESEND_API_KEY="re_test")
@pytest.mark.django_db
def test_contact_api_keeps_inquiry_when_smtp_fails(api_client):
    with patch(
        "apps.contact.services.email_notifications.resend.Emails.send",
        side_effect=OSError("Resend unavailable"),
    ):
        response = api_client.post("/api/contact/", VALID_PAYLOAD, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    inquiry = ContactInquiry.objects.get()
    assert inquiry.notification_sent_at is None
    assert inquiry.confirmation_sent_at is None
    assert "Resend unavailable" in inquiry.email_error


@pytest.mark.django_db
def test_contact_api_queues_email_delivery_by_default(api_client):
    with patch("apps.contact.api.views.queue_contact_emails") as queue_emails:
        response = api_client.post("/api/contact/", VALID_PAYLOAD, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    queue_emails.assert_called_once()
    assert queue_emails.call_args.args[0].pk == ContactInquiry.objects.get().pk
    assert queue_emails.call_args.args[1] == "en"


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
