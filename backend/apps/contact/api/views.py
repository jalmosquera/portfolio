from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle

from core.i18n import request_language

from ..models import ContactInquiry
from ..services.email_notifications import send_contact_emails
from .serializers import ContactInquirySerializer


class ContactInquiryCreateView(CreateAPIView):
    queryset = ContactInquiry.objects.all()
    serializer_class = ContactInquirySerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "contact"

    def perform_create(self, serializer):
        inquiry = serializer.save()
        send_contact_emails(inquiry, request_language(self.request))
