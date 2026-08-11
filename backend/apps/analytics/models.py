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
