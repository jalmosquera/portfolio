from calendar import monthrange
from datetime import timedelta

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from ..models import DailySiteVisit, SiteVisitCounter, analytics_today
from .serializers import VisitSummarySerializer


class IsSuperuser(BasePermission):
    message = "Superuser access is required."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class RecordVisitView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "visits"

    def post(self, request):
        SiteVisitCounter.record_visit()
        return Response(status=HTTP_204_NO_CONTENT)


class VisitSummaryView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsSuperuser]

    @staticmethod
    def _daily_series(visits_by_date, today, days=30):
        start = today - timedelta(days=days - 1)
        return [
            {
                "label": (start + timedelta(days=offset)).isoformat(),
                "visits": visits_by_date.get(start + timedelta(days=offset), 0),
            }
            for offset in range(days)
        ]

    @staticmethod
    def _weekly_series(visits_by_date, today, weeks=12):
        current_week = today - timedelta(days=today.weekday())
        first_week = current_week - timedelta(weeks=weeks - 1)
        series = []
        for offset in range(weeks):
            week_start = first_week + timedelta(weeks=offset)
            week_end = week_start + timedelta(days=6)
            total = sum(
                visits_by_date.get(week_start + timedelta(days=day), 0)
                for day in range(7)
            )
            series.append({"label": f"{week_start.isoformat()} / {week_end.isoformat()}", "visits": total})
        return series

    @staticmethod
    def _monthly_series(visits_by_date, today, months=12):
        month_starts = []
        year, month = today.year, today.month
        for _ in range(months):
            month_starts.append(today.replace(year=year, month=month, day=1))
            month -= 1
            if month == 0:
                month = 12
                year -= 1

        series = []
        for month_start in reversed(month_starts):
            days = monthrange(month_start.year, month_start.month)[1]
            total = sum(
                visits_by_date.get(month_start + timedelta(days=day), 0)
                for day in range(days)
            )
            series.append({"label": month_start.strftime("%Y-%m"), "visits": total})
        return series

    def get(self, request):
        today = analytics_today()
        history_start = today.replace(year=today.year - 1) if not (today.month == 2 and today.day == 29) else today.replace(year=today.year - 1, day=28)
        visits_by_date = dict(
            DailySiteVisit.objects.filter(date__gte=history_start, date__lte=today).values_list("date", "visits")
        )
        week_start = today - timedelta(days=today.weekday())
        month_start = today.replace(day=1)
        counter = SiteVisitCounter.objects.filter(pk=1).first()

        payload = {
            "today": visits_by_date.get(today, 0),
            "current_week": sum(
                visits for date, visits in visits_by_date.items() if week_start <= date <= today
            ),
            "current_month": sum(
                visits for date, visits in visits_by_date.items() if month_start <= date <= today
            ),
            "all_time": counter.total_visits if counter else 0,
            "daily": self._daily_series(visits_by_date, today),
            "weekly": self._weekly_series(visits_by_date, today),
            "monthly": self._monthly_series(visits_by_date, today),
        }
        response = Response(VisitSummarySerializer(payload).data)
        response["Cache-Control"] = "private, no-store"
        return response
