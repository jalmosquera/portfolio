from datetime import date, timedelta, timezone as datetime_timezone
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

from django.conf import settings
from django.db.models import Avg, Count, DurationField, ExpressionWrapper, F, Q
from django.db.models.functions import TruncDate, TruncMonth, TruncWeek
from django.utils import timezone

from .models import AnalyticsEvent, AnalyticsSession, DailySiteVisit, SiteVisitCounter, analytics_today


SESSION_TIMEOUT = timedelta(minutes=30)


def normalize_source(utm_source="", referrer=""):
    value = (utm_source or "").lower()
    host = urlparse(referrer or "").hostname or ""
    candidate = f"{value} {host}".lower()
    if not candidate.strip():
        return "Direct"
    if "google" in candidate:
        return "Google"
    if "linkedin" in candidate or "lnkd.in" in candidate:
        return "LinkedIn"
    if "github" in candidate:
        return "GitHub"
    return "Other"


def safe_country(request):
    value = request.META.get("HTTP_CF_IPCOUNTRY", "").upper()
    return value if len(value) == 2 and value.isalpha() and value not in {"XX", "T1"} else ""


def get_or_create_session(validated_data, country=""):
    now = timezone.now()
    visitor_id = validated_data["visitor_id"]
    session_id = validated_data.pop("session_id", None)
    existing = None
    if session_id:
        existing = AnalyticsSession.objects.filter(
            id=session_id,
            visitor_id=visitor_id,
            last_seen_at__gte=now - SESSION_TIMEOUT,
        ).first()
    if existing:
        existing.last_seen_at = now
        existing.save(update_fields=["last_seen_at"])
        return existing, False

    returning = AnalyticsSession.objects.filter(visitor_id=visitor_id).exists()
    session = AnalyticsSession.objects.create(
        **validated_data,
        country=country,
        source=normalize_source(validated_data.get("utm_source"), validated_data.get("referrer")),
        is_returning=returning,
        started_at=now,
        last_seen_at=now,
    )
    SiteVisitCounter.record_visit()
    return session, True


def record_event(validated_data):
    session = validated_data["session"]
    now = timezone.now()
    AnalyticsSession.objects.filter(pk=session.pk).update(last_seen_at=now)
    return AnalyticsEvent.objects.create(**validated_data, created_at=now)


def _period_series(queryset, today, truncation, count, unit):
    tz = ZoneInfo(settings.ANALYTICS_TIME_ZONE)
    grouped = {
        row["bucket"].date() if hasattr(row["bucket"], "date") else row["bucket"]: row
        for row in queryset.annotate(bucket=truncation("started_at", tzinfo=tz))
        .values("bucket")
        .annotate(visits=Count("id"), unique_visitors=Count("visitor_id", distinct=True))
        .order_by("bucket")
    }
    if unit == "day":
        start = today - timedelta(days=count - 1)
        buckets = [start + timedelta(days=index) for index in range(count)]
        labels = [bucket.isoformat() for bucket in buckets]
    elif unit == "week":
        current = today - timedelta(days=today.weekday())
        buckets = [current - timedelta(weeks=count - 1 - index) for index in range(count)]
        labels = [f"{bucket.isoformat()} / {(bucket + timedelta(days=6)).isoformat()}" for bucket in buckets]
    else:
        buckets = []
        year, month = today.year, today.month
        for _ in range(count):
            buckets.append(today.replace(year=year, month=month, day=1))
            month -= 1
            if month == 0:
                month, year = 12, year - 1
        buckets.reverse()
        labels = [bucket.strftime("%Y-%m") for bucket in buckets]
    return [
        {
            "label": label,
            "visits": grouped.get(bucket, {}).get("visits", 0),
            "unique_visitors": grouped.get(bucket, {}).get("unique_visitors", 0),
        }
        for bucket, label in zip(buckets, labels)
    ]


def _ranking(queryset, field, limit=10, label_fallback="Unknown"):
    return [
        {"label": row[field] or label_fallback, "value": row["value"]}
        for row in queryset.values(field).annotate(value=Count("id")).order_by("-value", field)[:limit]
    ]


def build_analytics_summary():
    today = analytics_today()
    tz = ZoneInfo(settings.ANALYTICS_TIME_ZONE)
    now = timezone.now()
    local_now = now.astimezone(tz)
    day_start = local_now.replace(hour=0, minute=0, second=0, microsecond=0).astimezone(datetime_timezone.utc)
    week_start = (local_now - timedelta(days=local_now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0).astimezone(datetime_timezone.utc)
    month_start = local_now.replace(day=1, hour=0, minute=0, second=0, microsecond=0).astimezone(datetime_timezone.utc)
    sessions = AnalyticsSession.objects.all()
    events = AnalyticsEvent.objects.all()
    pageviews = events.filter(event_type=AnalyticsEvent.EventType.PAGE_VIEW)

    session_count = sessions.count()
    pageview_count = pageviews.count()
    unique_visitors = sessions.values("visitor_id").distinct().count()
    duration = sessions.aggregate(
        average=Avg(ExpressionWrapper(F("last_seen_at") - F("started_at"), output_field=DurationField()))
    )["average"]
    bounced = sessions.annotate(
        pageview_count=Count("events", filter=Q(events__event_type=AnalyticsEvent.EventType.PAGE_VIEW))
    ).filter(pageview_count__lte=1).count()
    counter = SiteVisitCounter.objects.filter(pk=1).first()
    legacy_daily = dict(DailySiteVisit.objects.values_list("date", "visits"))

    event_counts = dict(events.values_list("event_type").annotate(total=Count("id")))
    daily = _period_series(sessions, today, TruncDate, 30, "day")
    weekly = _period_series(sessions, today, TruncWeek, 12, "week")
    monthly = _period_series(sessions, today, TruncMonth, 12, "month")
    if not session_count:
        for row in daily:
            row["visits"] = legacy_daily.get(date.fromisoformat(row["label"]), 0)

    return {
        "today": sessions.filter(started_at__gte=day_start).count() or legacy_daily.get(today, 0),
        "current_week": sessions.filter(started_at__gte=week_start).count() or sum(v for d, v in legacy_daily.items() if today - timedelta(days=today.weekday()) <= d <= today),
        "current_month": sessions.filter(started_at__gte=month_start).count() or sum(v for d, v in legacy_daily.items() if today.replace(day=1) <= d <= today),
        "all_time": counter.total_visits if counter else session_count,
        "unique_visitors": unique_visitors,
        "sessions": session_count,
        "pageviews": pageview_count,
        "pages_per_session": round(pageview_count / session_count, 2) if session_count else 0,
        "average_session_seconds": round(duration.total_seconds()) if duration else 0,
        "bounce_rate": round(bounced * 100 / session_count, 1) if session_count else 0,
        "new_visitors": sessions.filter(is_returning=False).values("visitor_id").distinct().count(),
        "returning_visitors": sessions.filter(is_returning=True).values("visitor_id").distinct().count(),
        "daily": daily,
        "weekly": weekly,
        "monthly": monthly,
        "sources": _ranking(sessions, "source", 5, "Direct"),
        "devices": _ranking(sessions, "device_type", 3),
        "browsers": _ranking(sessions, "browser", 8),
        "operating_systems": _ranking(sessions, "operating_system", 8),
        "countries": _ranking(sessions.exclude(country=""), "country", 10, "No data"),
        "top_pages": _ranking(pageviews.exclude(path=""), "path", 10),
        "top_projects": _ranking(events.filter(event_type=AnalyticsEvent.EventType.PROJECT_VIEW).exclude(target=""), "target", 10),
        "conversions": {
            event_type: event_counts.get(event_type, 0)
            for event_type in [
                AnalyticsEvent.EventType.CONTACT_CLICK,
                AnalyticsEvent.EventType.GITHUB_CLICK,
                AnalyticsEvent.EventType.LINKEDIN_CLICK,
                AnalyticsEvent.EventType.CV_DOWNLOAD,
            ]
        },
    }
