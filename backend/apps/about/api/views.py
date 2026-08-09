from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView

from ..models import About
from .serializers import AboutSerializer


class AboutView(RetrieveAPIView):
    serializer_class = AboutSerializer

    def get_object(self):
        return get_object_or_404(About, is_visible=True)
