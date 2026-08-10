from django.contrib import admin

from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ["public_filename", "download_count", "updated_at"]
    readonly_fields = ["download_count", "uploaded_at", "updated_at"]

    def has_add_permission(self, request):
        return not Resume.objects.exists()
