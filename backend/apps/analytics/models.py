import uuid
from zoneinfo import ZoneInfo

from django.conf import settings
from django.db import models, transaction
from django.db.models import F
from django.utils import timezone


def analytics_today():
    return timezone.localdate(timezone=ZoneInfo(settings.ANALYTICS_TIME_ZONE))


class SiteVisitCounter(models.Model):
    total_visits = models.PositiveBigIntegerField(default=0)
    first_visit_at = models.DateTimeField(null=True, blank=True)
    last_visit_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "site visit counter"
        verbose_name_plural = "site visit counter"

    def __str__(self):
        return f"{self.total_visits} visits"

    @classmethod
    def record_visit(cls):
        now = timezone.now()
        visit_date = analytics_today()
        with transaction.atomic():
            counter, created = cls.objects.select_for_update().get_or_create(
                pk=1,
                defaults={
                    "total_visits": 1,
                    "first_visit_at": now,
                    "last_visit_at": now,
                },
            )
            if not created:
                cls.objects.filter(pk=counter.pk).update(
                    total_visits=F("total_visits") + 1,
                    last_visit_at=now,
                )
                counter.refresh_from_db()

            daily_counter, daily_created = DailySiteVisit.objects.select_for_update().get_or_create(
                date=visit_date,
                defaults={"visits": 1},
            )
            if not daily_created:
                DailySiteVisit.objects.filter(pk=daily_counter.pk).update(visits=F("visits") + 1)
        return counter


class DailySiteVisit(models.Model):
    date = models.DateField(unique=True)
    visits = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ["-date"]
        verbose_name = "daily site visits"
        verbose_name_plural = "daily site visits"

    def __str__(self):
        return f"{self.date}: {self.visits} visits"


class AnalyticsSession(models.Model):
    class DeviceType(models.TextChoices):
        DESKTOP = "desktop", "Desktop"
        MOBILE = "mobile", "Mobile"
        TABLET = "tablet", "Tablet"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    visitor_id = models.UUIDField(db_index=True)
    started_at = models.DateTimeField(default=timezone.now, db_index=True)
    last_seen_at = models.DateTimeField(default=timezone.now, db_index=True)
    landing_path = models.CharField(max_length=512, blank=True)
    referrer = models.URLField(max_length=1000, blank=True)
    source = models.CharField(max_length=80, default="Direct", db_index=True)
    utm_source = models.CharField(max_length=160, blank=True)
    utm_medium = models.CharField(max_length=160, blank=True)
    utm_campaign = models.CharField(max_length=160, blank=True)
    device_type = models.CharField(max_length=16, choices=DeviceType.choices, default=DeviceType.DESKTOP)
    browser = models.CharField(max_length=80, blank=True)
    operating_system = models.CharField(max_length=80, blank=True)
    language = models.CharField(max_length=35, blank=True)
    country = models.CharField(max_length=2, blank=True)
    is_returning = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["-started_at"]
        indexes = [
            models.Index(fields=["visitor_id", "started_at"], name="analytics_visitor_started"),
            models.Index(fields=["source", "started_at"], name="analytics_source_started"),
        ]

    def __str__(self):
        return f"{self.visitor_id} · {self.started_at:%Y-%m-%d %H:%M}"


class AnalyticsEvent(models.Model):
    class EventType(models.TextChoices):
        PAGE_VIEW = "page_view", "Page view"
        PROJECT_VIEW = "project_view", "Project view"
        CONTACT_CLICK = "contact_click", "Contact click"
        GITHUB_CLICK = "github_click", "GitHub click"
        LINKEDIN_CLICK = "linkedin_click", "LinkedIn click"
        CV_DOWNLOAD = "cv_download", "CV download"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(AnalyticsSession, on_delete=models.CASCADE, related_name="events")
    event_type = models.CharField(max_length=32, choices=EventType.choices, db_index=True)
    path = models.CharField(max_length=512, blank=True, db_index=True)
    target = models.CharField(max_length=512, blank=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["event_type", "created_at"], name="analytics_event_created"),
            models.Index(fields=["path", "created_at"], name="analytics_path_created"),
        ]

    def __str__(self):
        return f"{self.event_type} · {self.path or self.target}"
