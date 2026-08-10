from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Project, ProjectContent




@admin.register(Project)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['title']
    search_fields = ['title']


@admin.register(ProjectContent)
class ProjectContentAdmin(TranslatableAdmin):
    list_display = ['project']


