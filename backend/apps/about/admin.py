from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import About


@admin.register(About)
class AboutAdmin(TranslatableAdmin):
    list_display = ["title", "is_visible", "updated_at"]
    list_filter = ["is_visible"]

    def has_add_permission(self, request):
        return not About.objects.exists()
