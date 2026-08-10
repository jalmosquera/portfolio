from django.contrib import admin

from .models import ContactInquiry


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ["company_or_recruiter", "email", "phone", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["company_or_recruiter", "email", "phone", "description"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
