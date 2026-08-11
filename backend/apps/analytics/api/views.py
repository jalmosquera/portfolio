from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from ..models import SiteVisitCounter
from ..services import build_analytics_summary, get_or_create_session, record_event, safe_country
from .serializers import AnalyticsEventSerializer, AnalyticsSessionSerializer, VisitSummarySerializer


class IsSuperuser(BasePermission):
    message = "Superuser access is required."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class RecordVisitView(APIView):
    """Legacy endpoint kept for backwards compatibility."""

    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "visits"

    def post(self, request):
        SiteVisitCounter.record_visit()
        return Response(status=HTTP_204_NO_CONTENT)


class AnalyticsSessionView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "analytics_sessions"

    def post(self, request):
        serializer = AnalyticsSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session, created = get_or_create_session(serializer.validated_data, safe_country(request))
        return Response({"session_id": str(session.id), "created": created}, status=HTTP_201_CREATED if created else 200)


class AnalyticsEventView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "analytics_events"

    def post(self, request):
        serializer = AnalyticsEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        record_event(serializer.validated_data)
        return Response(status=HTTP_201_CREATED)


class VisitSummaryView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsSuperuser]

    def get(self, request):
        response = Response(VisitSummarySerializer(build_analytics_summary()).data)
        response["Cache-Control"] = "private, no-store"
        return response
