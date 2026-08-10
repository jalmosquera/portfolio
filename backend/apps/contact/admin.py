from django.contrib import admin

from .models import ContactInquiry


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = [
        "company_or_recruiter",
        "email",
        "phone",
        "status",
        "notification_sent_at",
        "confirmation_sent_at",
        "created_at",
    ]
    list_filter = ["status", "notification_sent_at", "confirmation_sent_at", "created_at"]
    search_fields = ["company_or_recruiter", "email", "phone", "description"]
    readonly_fields = [
        "notification_sent_at",
        "confirmation_sent_at",
        "email_error",
        "created_at",
        "updated_at",
    ]
    ordering = ["-created_at"]
