from django.contrib import admin

from .models import SiteVisitCounter


@admin.register(SiteVisitCounter)
class SiteVisitCounterAdmin(admin.ModelAdmin):
    list_display = ["total_visits", "first_visit_at", "last_visit_at"]
    readonly_fields = ["total_visits", "first_visit_at", "last_visit_at"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
