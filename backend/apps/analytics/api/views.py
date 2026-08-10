from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from ..models import SiteVisitCounter


class RecordVisitView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "visits"

    def post(self, request):
        SiteVisitCounter.record_visit()
        return Response(status=HTTP_204_NO_CONTENT)
