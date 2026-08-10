from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import ProjectImage, ProjectImageContent


admin.site.register(ProjectImage)
admin.site.register(ProjectImageContent, TranslatableAdmin)
