import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone


logger = logging.getLogger(__name__)


def _message(*, subject, text, template, context, to, reply_to):
    message = EmailMultiAlternatives(
        subject=subject,
        body=text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to,
        reply_to=reply_to,
    )
    message.attach_alternative(render_to_string(template, context), "text/html")
    return message


def send_contact_emails(inquiry, language):
    if not settings.EMAIL_NOTIFICATIONS_ENABLED:
        return

    context = {
        "company_or_recruiter": inquiry.company_or_recruiter,
        "email": inquiry.email,
        "phone": inquiry.phone,
        "description": inquiry.description,
    }
    errors = []
    updates = {}

    notification = _message(
        subject=f"Nueva consulta del portfolio: {inquiry.company_or_recruiter}",
        text=(
            f"Empresa o reclutador: {inquiry.company_or_recruiter}\n"
            f"Email: {inquiry.email}\n"
            f"Teléfono: {inquiry.phone}\n\n"
            f"Descripción:\n{inquiry.description}"
        ),
        template="contact/ContactNotification.html",
        context=context,
        to=[settings.CONTACT_NOTIFICATION_EMAIL],
        reply_to=[inquiry.email],
    )
    try:
        notification.send(fail_silently=False)
        updates["notification_sent_at"] = timezone.now()
    except Exception as exc:  # SMTP failures must not discard the saved inquiry.
        logger.exception("Unable to send contact notification for inquiry %s", inquiry.pk)
        errors.append(f"notification: {exc}")

    is_spanish = language == "es"
    confirmation = _message(
        subject="Recibí tu mensaje" if is_spanish else "Your message was received",
        text=(
            f"Hola, {inquiry.company_or_recruiter}.\n\n"
            "Recibí correctamente tu mensaje y responderé lo antes posible."
            if is_spanish
            else f"Hello, {inquiry.company_or_recruiter}.\n\n"
            "Your message was received successfully. I will reply as soon as possible."
        ),
        template=(
            "contact/ContactConfirmationEs.html"
            if is_spanish
            else "contact/ContactConfirmationEn.html"
        ),
        context=context,
        to=[inquiry.email],
        reply_to=[settings.CONTACT_NOTIFICATION_EMAIL],
    )
    try:
        confirmation.send(fail_silently=False)
        updates["confirmation_sent_at"] = timezone.now()
    except Exception as exc:  # SMTP failures must not discard the saved inquiry.
        logger.exception("Unable to send contact confirmation for inquiry %s", inquiry.pk)
        errors.append(f"confirmation: {exc}")

    updates["email_error"] = "\n".join(errors)[:2000]
    type(inquiry).objects.filter(pk=inquiry.pk).update(**updates)
