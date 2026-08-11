from django.contrib import admin

from .models import AnalyticsEvent, AnalyticsSession, DailySiteVisit, SiteVisitCounter


@admin.register(SiteVisitCounter)
class SiteVisitCounterAdmin(admin.ModelAdmin):
    list_display = ["total_visits", "first_visit_at", "last_visit_at"]
    readonly_fields = ["total_visits", "first_visit_at", "last_visit_at"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DailySiteVisit)
class DailySiteVisitAdmin(admin.ModelAdmin):
    list_display = ["date", "visits"]
    date_hierarchy = "date"
    ordering = ["-date"]
    readonly_fields = ["date", "visits"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AnalyticsSession)
class AnalyticsSessionAdmin(admin.ModelAdmin):
    list_display = ["visitor_id", "started_at", "last_seen_at", "source", "device_type", "country", "is_returning"]
    list_filter = ["source", "device_type", "country", "is_returning", "started_at"]
    search_fields = ["visitor_id", "landing_path", "referrer", "utm_source", "utm_campaign"]
    readonly_fields = [field.name for field in AnalyticsSession._meta.fields]
    date_hierarchy = "started_at"

    def has_add_permission(self, request):
        return False


@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = ["event_type", "path", "target", "created_at"]
    list_filter = ["event_type", "created_at"]
    search_fields = ["path", "target", "session__visitor_id"]
    readonly_fields = [field.name for field in AnalyticsEvent._meta.fields]
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False
