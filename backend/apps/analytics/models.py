from django.db import models, transaction
from django.db.models import F
from django.utils import timezone


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
        return counter
