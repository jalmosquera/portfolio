from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import (
    Resume,
    ResumeContent,
    ResumeEducation,
    ResumeExperience,
    ResumeExperienceBullet,
    ResumeHighlight,
    ResumeSkill,
)


class ResumeChildAdmin(TranslatableAdmin):
    list_display = ["__str__", "resume", "order"]
    list_filter = ["resume"]
    ordering = ["resume", "order"]


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active", "download_count", "updated_at"]
    readonly_fields = ["download_count", "uploaded_at", "updated_at"]

    def has_add_permission(self, request):
        return not Resume.objects.exists()


@admin.register(ResumeContent)
class ResumeContentAdmin(TranslatableAdmin):
    list_display = ["resume", "__str__"]


@admin.register(ResumeHighlight)
class ResumeHighlightAdmin(ResumeChildAdmin):
    pass


@admin.register(ResumeSkill)
class ResumeSkillAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "resume", "order"]
    list_filter = ["resume", "category"]
    ordering = ["resume", "order"]


@admin.register(ResumeExperience)
class ResumeExperienceAdmin(ResumeChildAdmin):
    pass


@admin.register(ResumeExperienceBullet)
class ResumeExperienceBulletAdmin(ResumeChildAdmin):
    list_display = ["__str__", "experience", "resume", "order"]


@admin.register(ResumeEducation)
class ResumeEducationAdmin(ResumeChildAdmin):
    pass
