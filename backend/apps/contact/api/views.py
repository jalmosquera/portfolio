from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle

from ..models import ContactInquiry
from .serializers import ContactInquirySerializer


class ContactInquiryCreateView(CreateAPIView):
    queryset = ContactInquiry.objects.all()
    serializer_class = ContactInquirySerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "contact"
