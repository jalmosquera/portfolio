from rest_framework.generics import CreateAPIView
from rest_framework.throttling import ScopedRateThrottle

from ..models import ContactInquiry
from .serializers import ContactInquirySerializer


class ContactInquiryCreateView(CreateAPIView):
    queryset = ContactInquiry.objects.all()
    serializer_class = ContactInquirySerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "contact"
